import requests
import time
import math
from .math_prompt_config import MATH_INSTRUCTION_PROMPT,GSM8K_XL_PROMPT_SINGLESTEP, GSM8K_XL_PROMPT_MULTISTEPS, REACT_MATH_PROMPT, MATH_SPECULATIVE_INSTRUCTION_PROMPT


def math_action_parsing(actions):
    results = {}  # Dictionary to store the results of each action
    def split_operands(operands_str):
        # Custom split function to only split at commas not within brackets
        operands = []
        current_operand = []
        bracket_level = 0
        for char in operands_str:
            if char == '[':
                bracket_level += 1
                current_operand.append(char)
            elif char == ']':
                bracket_level -= 1
                current_operand.append(char)
            elif char == ',' and bracket_level == 0:
                operands.append(''.join(current_operand).strip())
                current_operand = []
            else:
                current_operand.append(char)
        operands.append(''.join(current_operand).strip())  # Add the last operand
        return operands
        
    def parse_operation(operation_with_operands):
        # Base case: If the operation is a direct value (no brackets indicating a nested operation)
        if not operation_with_operands.startswith("add") and not operation_with_operands.startswith("subtract") and not operation_with_operands.startswith("multiply") and not operation_with_operands.startswith("divide") and not operation_with_operands.startswith("Finish"):
            if isinstance(operation_with_operands, int) or isinstance(operation_with_operands, float):
                return float(operation_with_operands)
            elif "[" not in operation_with_operands:
                return float(operation_with_operands)
            else:
                # we need to calculate the value of the result
                stack = []
                operator_hold = ''
                for token in operation_with_operands.split():
                    if token.startswith("result"):
                        idx = token.split("[")[1].rstrip("]")
                        if idx in results and results[idx] is not None:
                            stack.append(results[idx])
                        else:
                            return None
                    elif token in ['+', '-', '*', '/']:
                        operator_hold = token
                    else:
                        stack.append(float(token))
                if operator_hold == '+':
                    return stack[0] + stack[1]
                elif operator_hold == '-':
                    return stack[0] - stack[1]
                elif operator_hold == '*':
                    return stack[0] * stack[1]
                elif operator_hold == '/':
                    return stack[0] / stack[1]
        # Recursive case: Parse a nested operation
        operation, operands_str = operation_with_operands.split("[", 1)
        operands_str = operands_str.rsplit("]", 1)[0]
        operands = split_operands(operands_str)
        operands_values = []

        for operand in operands:
            if "[" in operand:
                if operand.startswith("result"):
                    # Replace the result index with the actual value
                    result_index = operand.split("[")[1].rstrip("]")
                    if result_index in results and results[result_index] is not None:
                        operand = results[result_index]
                    else:
                        return None
                else:
                    # Recursively parse the nested operation
                    operand = parse_operation(operand)
                operands_values.append(operand)
            else:
                # Directly parse the operand
                operands_values.append(float(operand))
        final_result = perform_operation(operation, operands_values)
        # print(f"{operation_with_operands}=={final_result}")
        # Perform the operation with the evaluated operands
        return final_result
    
    def perform_operation(operation, operands):
        if operation == "add":
            return sum(operands)
        elif operation == "subtract":
            return operands[0] - operands[1]
        elif operation == "multiply":
            result = 1
            for value in operands:
                result *= value
            return result
        elif operation == "divide":
            return operands[0] / operands[1]
        elif operation == "Finish":
            return operands[0]
        else:
            raise ValueError(f"Unsupported operation: {operation}")
    for i in range(len(actions)):
        for action in actions:
            action = action.strip()
            result_index, operation_with_operands = action.split(" = ")
            result_index = result_index.split("[")[1].rstrip("]")
            # Directly parse and evaluate the operation, whether simple or nested
            results[result_index] = parse_operation(operation_with_operands)
    for action in actions:
            action = action.strip()
            result_index, operation_with_operands = action.split(" = ")
            result_index = result_index.split("[")[1].rstrip("]")
    # Assuming the last action's result is what we want to return
    if results:
        last_key = list(results.keys())[-1]
        return results[last_key], results
    else:
        return None, None
    

class math_request:
    def __init__(self, id, question, small_model_steps="", spec_result=True):
        self.id = id
        self.step = 1
        self.finished = False
        self.question = question

        if spec_result:
            self.prefix = MATH_SPECULATIVE_INSTRUCTION_PROMPT + "\nQuestion: "
            self.prompt_offset = len(MATH_SPECULATIVE_INSTRUCTION_PROMPT)
            self.prompt = self.prefix + question
        else:
            self.prefix = MATH_INSTRUCTION_PROMPT + REACT_MATH_PROMPT + "\nQuestion: "
            self.prompt_offset = len(MATH_INSTRUCTION_PROMPT + REACT_MATH_PROMPT)
            self.prompt = self.prefix + question

    
    def record_time(self, type=0):
        if type == 0:
            self.start_time = time.time()
        else:
            self.end_time = time.time()
            self.latency = self.end_time - self.start_time

    def extend_thought(self, thought):
        self.prompt += thought.replace("\n", "") + "\n" # thought has the prefix "Thought {self.step}:"

    def extend_action(self, action):
        self.prompt += f"Action {self.step}: {action}\n"

    def extend_observation(self, result):
        self.prompt += f"Observation {self.step}: The result is {result}\n"
        self.step += 1

    def finish(self):
        self.prompt += f"Action {self.step}: Finish[None]\n"
        self.finished = True

    def print_prompt(self):
        print(self.prompt[self.prompt_offset:])

    def write_promt_to_file(self, file_name):
        with open(file_name, "a") as f:
            f.write(self.prompt[self.prompt_offset:] + "\n=======================================================\n")
            f.close()