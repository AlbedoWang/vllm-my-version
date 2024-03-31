# Tools Augmented vLLM

## Preserve
Currntly not finished, just update a stable version without Preserve

## Swap Pipeline
Changed in :
- engine
  - arg\_utils.py
  - llm\_engine.py
- model\_excutor
  - models
    - llama.py
- transformers\_utils
  - config.py
  - tokenizer.py
- worker
  - cache\_engine.py
  - model\_runner.py
  - worker.py
- offline\_inference.py
- testmath.py

Currntly not stable, just update a stable version without swap pipeline

Almost all stable changes begin with "# NOTE(KJ.W)"

IF want to run code, please use special conda env (vllm-cu124)
