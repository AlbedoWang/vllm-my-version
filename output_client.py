from multiprocessing.managers import BaseManager
from vllm import LLM, SamplingParams
import time
import argparse
import os
import sys
import pickle
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from test_math_utils.math_utils import *
from datetime import datetime
import re

class LLMEngineManager(BaseManager):
    pass

LLMEngineManager.register('LLMEngineProxy')

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


if __name__ == "__main__":
    LLMmanager = LLMEngineManager(
        address=('localhost', 50000),
        authkey=b'password'
    )
    LLMmanager.connect()
    llm_engine_proxy = LLMmanager.LLMEngineProxy()

    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["GET_LLAMA_INFO"] = "0"
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

    i = 0
    while True:
        llm_engine_proxy.get_output()

    
def math_action_parsing(thought_action, this_request):
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