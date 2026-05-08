"""Speed probe — checks inference tok/s with current env."""
import os
os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["UNSLOTH_COMPILE_DISABLE"] = "1"
import torch._inductor.config  # noqa: F401

import unsloth  # noqa: F401 — must import first
import time

import torch
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

# Realistic probe — open-ended, similar to soul probes
prompt = "A friend asks for your honest opinion on their work. It's mediocre. What do you say?"
messages = [{"role": "user", "content": prompt}]
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

# First generation — includes any compile warm-up
print("\nGen 1 (cold, up to 400 tokens):")
t0 = time.time()
with torch.no_grad():
    out = model.generate(
        **inputs,
        max_new_tokens=400,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
    )
duration = time.time() - t0
gen_tokens = out.shape[1] - inputs["input_ids"].shape[1]
print(f"  {gen_tokens} tokens in {duration:.2f}s = {gen_tokens/duration:.1f} tok/s")

# Second generation — should be post-warmup
print("\nGen 2 (warm, up to 400 tokens):")
t0 = time.time()
with torch.no_grad():
    out = model.generate(
        **inputs,
        max_new_tokens=400,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
    )
duration = time.time() - t0
gen_tokens = out.shape[1] - inputs["input_ids"].shape[1]
print(f"  {gen_tokens} tokens in {duration:.2f}s = {gen_tokens/duration:.1f} tok/s")

response = tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
print(f"\nsample response:\n{response[:400]}")
