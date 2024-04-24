import sys
# sys.path.append('../')
import argparse
import os
from vllm import LLM, SamplingParams
import pickle
import time
import json
# from utils.hotpotqa_utils import hotpotqa_request, search_step, action_parsing
# from utils.prompt_config import SPECULATIVE_INSTRUCTION_PROMPT, ENHANCED_REACT_INSTRUCTION_PROMPT, ENHANCED_HOTPOTQA_PROMPT
# from utils.hotpotqa_speculative_utils import hotpotqa_speculative_output_parsing
from concurrent.futures import ProcessPoolExecutor, as_completed
from test_math_utils.math_utils import *
from datetime import datetime
import re
from collections import deque

# NOTE(KJ.W): Import multiprocessing
from multiprocessing import Process
from multiprocessing.managers import BaseManager

import random

from vllm.sequence import SequenceStatus

parser = argparse.ArgumentParser()
parser.add_argument("--n_initial", type=int, default=3, help="number of initial requests in the queue.")
parser.add_argument("--n_input", type=int, default=10, help="number of total requests.")
parser.add_argument("--temperature", type=float, default=0, help="temperature for sampling.")
parser.add_argument("--top_p", type=float, default=1, help="top_p for sampling.")
parser.add_argument("--max_tokens", type=int, default=1024, help="max_tokens for sampling.")
parser.add_argument("--step_upperbound", type=int, default=12, help="maximum number of steps for each request.")
parser.add_argument("--search_upperbound", type=int, default=3, help="maximum number of steps search for each request.")
parser.add_argument("--spec_upperbound", type=int, default=2, help="maximum number of speculative of each request.")
parser.add_argument("--if_speculative", action='store_true', help="if doing speculative")
parser.add_argument("--model", type=str, default="7", help="model size")
parser.add_argument('--quantized', action='store_true', help="if quantized model is used")
parser.add_argument("--rps", type=int, default=2, help="request per second")
parser.add_argument("--nGPU", type=int, default=1, help="GPU nums")
parser.add_argument("--kv_cache_ratio", type=float, default=-1.0, help="manually set the kv_cache_ratio for computing the number of kv cache block")
parser.add_argument("--prefix_cache", type=bool, default=False, help="enable prefix caching")
parser.add_argument("--device", type=str, default="cuda", help="set device name")


class LLMEngineProxy:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LLMEngineProxy, cls).__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(
        self, 
        model_name="meta-llama/Llama-2-7b-chat-hf",
        ):
        self.use_preserve = False
        self.use_swap = True
        self.requests_time_dict = {}
        
        if not hasattr(self, "initialized"):
            os.environ["TOKENIZERS_PARALLELISM"] = "false"
            os.environ["GET_LLAMA_INFO"] = "0"
            args = parser.parse_args()    
            # self.engine = LLM(model=model_name, enforce_eager=True, enable_prefix_caching=False,)
            self.engine = LLM(
                model="meta-llama/Llama-2-7b-chat-hf", 
                enforce_eager=True, 
                tensor_parallel_size=args.nGPU, 
                enable_prefix_caching= True, #self.use_preserve, 
                device=args.device,
                use_preserve=self.use_preserve,
                use_swap=self.use_swap,)
            self.initialized = True
            self.requests_dict = {}
            self.output_dict = {}
            self.output_queue = deque()
    
    def add_request(self, request_id, prompt, sampling_params, decision=None):
        self.requests_time_dict[request_id] = time.monotonic()
        self.engine.llm_engine.add_request(request_id, prompt, sampling_params, decision)     
    
    def math_action_parsing(self, thought_action, this_request):
        step = this_request.step
        try:
            thought, action = thought_action.strip().split(f"Action {step}: ")
            if action.startswith("Add"):
                action_type = 1
                offset = 4
            elif action.startswith("Multiply"):
                action_type = 2
                offset = 9
            elif action.startswith("Subtract"):
                action_type = 3
                offset = 9
            elif action.startswith("Divide"):
                action_type = 4
                offset = 7            
            elif action.startswith("Finish"):
                action_type = 5
                offset = 7
            else:
                print("[No Match]Error: action parsing failed.", "\n\n", thought, action, step, "\n\n")
                return 0, [None]
            numbers = action[offset:-1]
            number_list = numbers.split(",")
            number_list = [int(x) if x.isdigit() else float(x) for x in number_list]
            this_request.extend_thought(thought)
            this_request.extend_action(action)
            return action_type, number_list
        except:
            print("[ERROR]Error: action parsing failed.", "\n\n", "thought_action", thought_action, "step", step, "\n\n")
            # print("[*] Prompt: ", this_request.prompt)
            return 0, [None]
    
    def calculator(self, action, number_list):
        if action == 1:
            return sum(number_list)
        elif action == 2:
            result = 1
            for value in number_list:
                result *= value
            return result
        elif action == 3:
            return number_list[0] - number_list[1]
        elif action == 4:
            if number_list[1] == 0:
                return None
            return number_list[0] / number_list[1]
        elif action == 5:
            return number_list[0]
        else:
            return None
    
    def get_request_output(self):
        start_time = time.time()
        output_text = ""
        use_preserve = self.use_preserve
        use_swap = self.use_swap
        n_finished = 0
        args = parser.parse_args()
        temperature = args.temperature
        top_p = args.top_p
        max_tokens = args.max_tokens
        while self.engine.llm_engine.has_unfinished_requests():
            step_outputs = self.engine.llm_engine.step()
            for output in step_outputs:
                if output.finished:
                    res = output
                    print("[*]Current request id:", res.request_id)
                    output_text = output.outputs[0].text
                    output_request_id = str(output.request_id)
                    # self.output_dict[output_request_id] = output
                    self.output_queue.append((output_request_id, output))
        end_time = time.time()
        return output_text, end_time - start_time
    
    def get_output(self):
        args = parser.parse_args()
        use_preserve = self.use_preserve
        use_swap = self.use_swap
        temperature = args.temperature
        top_p = args.top_p
        max_tokens = args.max_tokens
        # if self.output_dict:
            # output_request_id, output = self.output_dict.popitem()
        if self.output_queue:
            print("[*] current output queue: ", [x[0] for x in self.output_queue])
            output_request_id, output = self.output_queue.popleft()
            if output_request_id not in self.requests_dict:
                this_request = math_request(output_request_id, "")
                this_request.prompt = output.prompt
                self.requests_dict[output_request_id] = this_request
            else:
                this_request = self.requests_dict[output_request_id]
            
            # time.sleep(4)
            
            action_type, number_list = self.math_action_parsing(output.outputs[0].text, this_request)
            
            if action_type == 5: # finish
                this_request.finish()
                this_time = time.monotonic()
                print("[*] Request Finished: ", output_request_id, " Processing Time: ",  this_time - self.requests_time_dict[output_request_id])
                self.requests_time_dict.pop(output_request_id)
                self.requests_dict.pop(output_request_id)
                self.engine.llm_engine.remove_paused_seq_group(this_request.id)
                print("Finish the request: ID-{}; Answer:{}; Label:{}".format(this_request.id, number_list[0], 'NOT DEFINED'))
                print("[*]Current llm engine schedule:"
                        f"\n\t- Running: {len(self.engine.llm_engine.scheduler.running), [x.request_id for x in self.engine.llm_engine.scheduler.running]}"
                        f"\n\t- Paused: {len(self.engine.llm_engine.scheduler.paused), [x.request_id for x in self.engine.llm_engine.scheduler.paused]}")
            elif action_type == 0 or action_type > 5:
                this_request.finish()
                this_time = time.monotonic()
                print("[*] Request Finished: ", output_request_id, " Processing Time: ",  this_time - self.requests_time_dict[output_request_id])
                self.requests_time_dict.pop(output_request_id)
                self.requests_dict.pop(output_request_id)
                self.engine.llm_engine.remove_paused_seq_group(this_request.id)
                print("Request Parsing ERROR ID-{}".format(this_request.id))
                print("[*]Current llm engine schedule:"
                        f"\n\t- Running: {len(self.engine.llm_engine.scheduler.running), [x.request_id for x in self.engine.llm_engine.scheduler.running]}"
                        f"\n\t- Paused: {len(self.engine.llm_engine.scheduler.paused), [x.request_id for x in self.engine.llm_engine.scheduler.paused]}")
            elif this_request.step > args.step_upperbound:
                n_finished += 1
                this_request.finish()
                this_time = time.monotonic()
                print("[*] Request Finished: ", output_request_id, " Processing Time: ",  this_time - self.requests_time_dict[output_request_id])
                self.requests_time_dict.pop(output_request_id)
                self.requests_dict.pop(output_request_id)
                self.engine.llm_engine.remove_paused_seq_group(this_request.id)
                print("Request ERROR Step upper bound ID-{}".format(this_request.id))
                print("[*]Current llm engine schedule:"
                        f"\n\t- Running: {len(self.engine.llm_engine.scheduler.running), [x.request_id for x in self.engine.llm_engine.scheduler.running]}"
                        f"\n\t- Paused: {len(self.engine.llm_engine.scheduler.paused), [x.request_id for x in self.engine.llm_engine.scheduler.paused]}")
            else: # call the calculator
                result = self.calculator(action_type, number_list)
                this_request.extend_observation(result)
                sampling_params = SamplingParams(temperature=temperature, top_p=top_p, max_tokens=max_tokens, stop=[f"\nObservation {this_request.step}:"])

                # if not use_preserve and not use_swap:
                #     self.engine.llm_engine.add_request(this_request.id, this_request.prompt, sampling_params)
                # elif use_swap:
                #     self.engine.llm_engine.swap_in_paused_requests(this_request.id, this_request.prompt, sampling_params)
                # else:
                #     self.engine.llm_engine.update_paused_request(this_request.id, this_request.prompt, sampling_params)
                
                self.engine.llm_engine.reactivate_sequence(this_request.id, this_request.prompt, sampling_params)

                print("[*]Current llm engine schedule:"
                        f"\n\t- Running: {len(self.engine.llm_engine.scheduler.running), [x.request_id for x in self.engine.llm_engine.scheduler.running]}"
                        f"\n\t- Paused: {len(self.engine.llm_engine.scheduler.paused), [x.request_id for x in self.engine.llm_engine.scheduler.paused]}")
        

class LLMEngineManager(BaseManager):
    pass

LLMEngineManager.register(
    'LLMEngineProxy', 
    callable=lambda: LLMEngineProxy()
    )

def manager_proxy():
    manager = LLMEngineManager(
        address=('localhost', 50000),
        authkey=b'password'
    )
    print("Starting manager server...")
    manager.start()
    print("Manager server started. Press Ctrl+C to exit.")
    try:
        llm_engine_proxy = manager.LLMEngineProxy()
        while True:
            output, process_time = llm_engine_proxy.get_request_output()
    except KeyboardInterrupt:
        print("Manager server shutting down...")

def run():
# if __name__ == "__main__":
    # Process(target=manager_proxy).start()
    manager_proxy()



def get_request_output(llm):
    start_time = time.time()
    output_text = ""
    output_list = []
    while llm.llm_engine.has_unfinished_requests():
        step_outputs = llm.llm_engine.step()
        for output in step_outputs:
            if output.finished:
                res = output
                print("[*]Current request id:", res.request_id)
                output_text = output.outputs[0].text
                output_id = output.request_id
                # NOTE(KJ.W): Change in generation
                end_time = time.time()
                output_list.append((output_text, end_time - start_time, output_id))
    # return output_text, end_time - start_time, output_id
    return output_list


def math_action_parsing(thought_action, this_request):
    step = this_request.step
    try:
        thought, action = thought_action.strip().split(f"Action {step}: ")

        # print("[*]Thought: ", thought)
        # print("[*]Action: ", action)

        # parse the action
        if action.startswith("Add"):
            action_type = 1
            offset = 4
        elif action.startswith("Multiply"):
            action_type = 2
            offset = 9
            
        elif action.startswith("Subtract"):
            action_type = 3
            offset = 9
        elif action.startswith("Divide"):
            action_type = 4
            offset = 7            
        elif action.startswith("Finish"):
            action_type = 5
            offset = 7
        else:
            print("[No Match]Error: action parsing failed.", "\n\n", thought, action, step, "\n\n")
            return 0, [None]
        numbers = action[offset:-1]
        number_list = numbers.split(",")
        number_list = [int(x) if x.isdigit() else float(x) for x in number_list]
        this_request.extend_thought(thought)
        this_request.extend_action(action)
        return action_type, number_list
    except:
        print("[ERROR]Error: action parsing failed.", "\n\n", "thought_action", thought_action, "step", step, "\n\n")
        return 0, [None]
    
def calculator(action, number_list):
    if action == 1:
        return sum(number_list)
    elif action == 2:
        result = 1
        for value in number_list:
            result *= value
        return result
    elif action == 3:
        return number_list[0] - number_list[1]
    elif action == 4:
        if number_list[1] == 0:
            return None
        return number_list[0] / number_list[1]
    elif action == 5:
        return number_list[0]
    else:
        return None


    
if __name__ == "__main__":
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["GET_LLAMA_INFO"] = "0"
    os.environ["CUDA_VISIBLE_DEVICES"]= "1"
    args = parser.parse_args()

    temperature = args.temperature
    top_p = args.top_p
    max_tokens = args.max_tokens

    input_file = "/home/kaijian_wang/vllm-my-version/math_data/sample_gsm8k-xl.json"
    row_input = json.load(open(input_file))
    inputs_and_answer = []
    for data in row_input:
        question = data.get("question", "")
        result = data.get("result", "")
        inputs_and_answer.append((question, result))

    request_table = {} 
    n_finished = 0
    n_correct = 0
    total_latency = 0.0
    total_step = 0
    request_log_list = []

    use_preserve = False
    use_swap = True

    # assert not (use_preserve and use_swap)

    if args.quantized:
        model_name = "llama-2-{}B-Chat-AWQ".format(args.model)
        model_dir = "/global/cfs/cdirs/m4243/Zheng/huggingface_llama_model/Llama-2-{}B-Chat-AWQ".format(args.model)
    else:
        model_name = "llama-2-{}b-chat-hf".format(args.model)
        model_dir = "/global/cfs/cdirs/m4243/Zheng/huggingface_llama_model/Llama-2-{}b-chat-hf".format(args.model)

    model_name = "meta-llama/Llama-2-7b-chat-hf"
    model_dir = None

    llm = LLM(
        model="meta-llama/Llama-2-7b-chat-hf", 
        enforce_eager=True, 
        tensor_parallel_size=args.nGPU, 
        enable_prefix_caching=use_preserve, 
        device=args.device,
        use_preserve=use_preserve,
        use_swap=use_swap,)

    
    for i in range(10):
        question = inputs_and_answer[i][0]
        answer = inputs_and_answer[i][1]
        request_id = str(next(llm.request_counter))    

        this_request = math_request(request_id, question, spec_result=False)

        sampling_params = SamplingParams(temperature=temperature, top_p=top_p, max_tokens=max_tokens, stop=[f"\nObservation {this_request.step}:"])
        llm.llm_engine.add_request(this_request.id, this_request.prompt, sampling_params)

        start_time = time.time()
        while llm.llm_engine.has_unfinished_requests():
            for output, llm_latency, output_id in get_request_output(llm):

                output_seq = llm.llm_engine.scheduler.get_paused_group(output_id)
                seq = output_seq.get_seqs()[0]
                current_blocktable = llm.llm_engine.scheduler.block_manager.block_tables[seq.seq_id]
                print(f"[*] current block table {output_id}: ", current_blocktable)

                action_type, number_list = math_action_parsing(output, this_request)

                if action_type == 5: # finish
                    n_finished += 1
                    this_request.finish()
                    if abs(number_list[0] - answer) < 1e-3:
                        if_acc = True
                        n_correct += 1

                    # NOTE(KJ.W): Remove the paused sequence group
                    llm.llm_engine.remove_paused_seq_group(this_request.id)
                    print("Finish the request: ID-{}; Answer:{}; Label:{}".format(this_request.id, number_list[0], answer))
                elif action_type == 0 or action_type > 5:
                    n_finished += 1
                    this_request.finish()
                    llm.llm_engine.remove_paused_seq_group(this_request.id)
                    print("Request Parsing ERROR ID-{}".format(this_request.id))
                elif this_request.step > args.step_upperbound:
                    n_finished += 1
                    this_request.finish()
                    llm.llm_engine.remove_paused_seq_group(this_request.id)
                    print("Request ERROR Step upper bound ID-{}".format(this_request.id))
                else: # call the calculator
                    result = calculator(action_type, number_list)
                    this_request.extend_observation(result)
                    sampling_params = SamplingParams(temperature=temperature, top_p=top_p, max_tokens=max_tokens, stop=[f"\nObservation {this_request.step}:"])
                    print("[*]Current llm engine schedule:"
                        f"\n\t- Running: {len(llm.llm_engine.scheduler.running), [x.request_id for x in llm.llm_engine.scheduler.running]}"
                        f"\n\t- Paused: {len(llm.llm_engine.scheduler.paused), [x.request_id for x in llm.llm_engine.scheduler.paused]}")

                    if not use_preserve and not use_swap:
                        llm.llm_engine.add_request(this_request.id, this_request.prompt, sampling_params)
                    elif use_swap:
                        llm.llm_engine.swap_in_paused_requests(this_request.id, this_request.prompt, sampling_params)
                    else:
                        llm.llm_engine.update_paused_request(this_request.id, this_request.prompt, sampling_params)


                    # print("[*]Current llm engine schedule(After update):"
                    #     f"\n\t- Running: {len(llm.llm_engine.scheduler.running)}"
                    #     f"\n\t- Paused: {len(llm.llm_engine.scheduler.paused)}"
                    #     f"\n\t- Waiting: {len(llm.llm_engine.scheduler.waiting)}")
                    # print("================================================\n")
        
        end_time = time.time()
        request_latency = end_time - start_time
        total_latency += request_latency
        total_step += this_request.step
        print("Request ID-{}; Latency:{}".format(this_request.id, end_time - start_time))
        request_log_list.append((this_request.id, if_acc, this_request.step, request_latency, answer, number_list[0]))

    output_file = "/home/kaijian_wang/vllm-my-version/react_result/react_{}_result_pid-{}-time-{}.txt".format(model_name.split('/')[-1], os.getpid(), datetime.now().strftime("%m-%d-%H-%M"))
    with open(output_file, "w+") as f:
        f.write("id, if_acc, step, latency, label, answer\n")
        for line in request_log_list:
            f.write(", ".join(str(x) for x in line) + "\n")

        print("n_test:{}, Accuracy:{:.3f}, avg_step:{:.3f}, avg_latency:{:.3f}".format(n_finished, n_correct/n_finished, total_step/n_finished, total_latency/n_finished))
        f.write("n_test:{}, Accuracy: {:.3f}, avg_step:{:.3f}, avg_latency:{:.3f}\n".format(n_finished, n_correct/n_finished, total_step/n_finished, total_latency/n_finished))

