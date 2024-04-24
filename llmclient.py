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
        if i >= 30:
            break
        time.sleep(1)

        question = inputs_and_answer[i][0]
        answer = inputs_and_answer[i][1]
        request_id = str(i)    

        this_request = math_request(request_id, question, spec_result=False)

        sampling_params = SamplingParams(temperature=temperature, top_p=top_p, max_tokens=max_tokens, stop=[f"\nObservation {this_request.step}:"])
        llm_engine_proxy.add_request(this_request.id, this_request.prompt, sampling_params)
        i += 1

    
