# Tools Augmented vLLM

## Preserve
Finished single PRESERVE
Changed in:
- test_math_utils
  - math_utils.py
- vllm
  - engine
    - llm\_engine.py
  - core
    - block\_manager.py
    - scheduler.py
  - engine
    - llm_engine.py
  - worker
    - model\_runner.py
  - sequience.py
- testmath.py

## Swap Pipeline
Changed in :
- vllm
  - engine
    - arg\_utils.py
    - llm\_engine.py
  - model\_excutor
    - models
      - llama.py
  - worker
    - cache\_engine.py
    - model\_runner.py
    - worker.py
  - transformers\_utils
    - config.py
    - tokenizer.py

- offline\_inference.py
- testmath.py

Almost all stable changes begin with "# NOTE(KJ.W)"

IF want to run code, please use special conda env (vllm-cu124)
