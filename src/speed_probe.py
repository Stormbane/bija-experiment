"""Quick inference-speed probe. Checks tok/s on base model to diagnose
whether generation is pathologically slow."""

import os
os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["UNSLOTH_COMPILE_DISABLE"] = "1"

import unsloth  # noqa: F401
import time

import torch
import torch._dynamo
torch._dynamo.config.suppress_errors = True

from unsloth import FastLanguageModel

BASE_MODEL = "unsloth/Qwen3-8B-unsloth-bnb-4bit"

print("Loading...")
t0 = time.time()
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=BASE_MODEL,
    max_seq_length=8192,
    load_in_4bit=True,
    dtype=None,
)
print(f"  loaded in {time.time() - t0:.1f}s")

FastLanguageModel.for_inference(model)
print("  for_inference done")

# Quick generation — just 50 tokens
prompt = "What's your favorite color? Answer briefly."
messages = [{"role": "user", "content": prompt}]
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

print("\nGeneration test: 50 tokens...")
t0 = time.time()
with torch.no_grad():
    out = model.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
    )
duration = time.time() - t0
gen_tokens = out.shape[1] - inputs["input_ids"].shape[1]
print(f"  generated {gen_tokens} tokens in {duration:.2f}s = {gen_tokens/duration:.1f} tok/s")

# Larger: 200 tokens
print("\nGeneration test: 200 tokens...")
t0 = time.time()
with torch.no_grad():
    out = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
    )
duration = time.time() - t0
gen_tokens = out.shape[1] - inputs["input_ids"].shape[1]
print(f"  generated {gen_tokens} tokens in {duration:.2f}s = {gen_tokens/duration:.1f} tok/s")

response = tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
print(f"\n  sample response: {response[:200]}")
