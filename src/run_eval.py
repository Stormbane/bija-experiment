"""Generate responses for each model × probe.

Loads base model once, then applies each LoRA adapter in turn. For each model,
generates responses to all soul probes with the appropriate system prompt
(bija × N for variants, none for base). Saves raw responses to
data/results/{model}/responses.json.
"""

# Disable torch.compile / dynamo — same issue as training with triton 3.6
import os
os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["UNSLOTH_COMPILE_DISABLE"] = "1"

# unsloth_zoo introspects torch._inductor.config at import time; the submodule
# must be explicitly imported or it's not an attribute of torch._inductor
import torch._inductor.config  # noqa: F401

import unsloth  # noqa: F401 — must import before transformers

import gc
import json
import re
import subprocess
import time
from pathlib import Path

# Qwen3's default chat template lets the model think before answering
# (wrapping output in <think>...</think>). That burns tokens and adds noise
# to behavioral measurement. We turn it off at the template level AND strip
# any residual tags as belt-and-suspenders.
THINK_STRIP_RE = re.compile(r"<think>.*?</think>\s*", re.DOTALL)

import torch
import torch._dynamo
torch._dynamo.config.suppress_errors = True

import yaml

import argparse

ROOT = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "config" / "experiment.yml"
DEFAULT_PROBES_PATH = ROOT / "data" / "probes" / "soul_probes.yml"
RESULTS_ROOT = ROOT / "data" / "results"
MODELS_ROOT = ROOT / "models"
RESULTS_SUFFIX = ""  # overridden by --suffix flag in main()

GEN_SETTINGS = {
    "max_new_tokens": 400,
    "do_sample": True,
    "temperature": 0.7,
    "top_p": 0.9,
    "repetition_penalty": 1.1,
}


def gpu_temp() -> int:
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits", "-i", "0"],
            capture_output=True, text=True, timeout=5,
        )
        return int(result.stdout.strip().split("\n")[0])
    except Exception:
        return -1


def load_probes(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_system_prompt(bija: str, repetitions: int) -> str:
    return " ".join([bija] * repetitions)


def generate_for_model(model_label: str, model, tokenizer, probes, system_prompt: str | None):
    """Generate response to each probe. Returns list of {id, domain, probe, response, gen_tokens}."""
    from unsloth import FastLanguageModel
    FastLanguageModel.for_inference(model)

    out = []
    t0 = time.time()
    for i, probe in enumerate(probes):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": probe["probe"]})

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,  # Qwen3: skip <think>...</think> prelude
        )
        inputs = tokenizer(text, return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                **GEN_SETTINGS,
                pad_token_id=tokenizer.eos_token_id,
            )

        # Extract only the generated portion
        gen_ids = outputs[0][inputs["input_ids"].shape[1]:]
        response = tokenizer.decode(gen_ids, skip_special_tokens=True).strip()
        # Belt-and-suspenders: strip any residual think tags the model emitted anyway
        response = THINK_STRIP_RE.sub("", response).strip()

        out.append({
            "id": probe["id"],
            "domain": probe["domain"],
            "probe": probe["probe"],
            "response": response,
            "gen_tokens": len(gen_ids),
        })

        # Periodic progress (every 5 probes so we actually see movement)
        if (i + 1) % 5 == 0 or i == len(probes) - 1:
            elapsed = time.time() - t0
            avg = elapsed / (i + 1)
            remaining = avg * (len(probes) - i - 1)
            print(f"  [{model_label}] {i+1}/{len(probes)} ({avg:.1f}s/probe, "
                  f"~{remaining/60:.1f} min remaining, GPU {gpu_temp()}°C)",
                  flush=True)

    duration = time.time() - t0
    print(f"  [{model_label}] done in {duration/60:.1f} min")
    return out


def eval_base(config, probes):
    """Evaluate base model with no system prompt."""
    from unsloth import FastLanguageModel

    print(f"\n{'=' * 60}\nEVAL: base (no adapter, no system prompt)\n{'=' * 60}")
    print(f"  GPU temp start: {gpu_temp()}°C")

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=config["base_model"],
        max_seq_length=config["training"]["max_seq_length"],
        load_in_4bit=True,
        dtype=None,
    )

    responses = generate_for_model("base", model, tokenizer, probes, system_prompt=None)

    out_dir = RESULTS_ROOT / f"base{RESULTS_SUFFIX}"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "responses.json", "w", encoding="utf-8") as f:
        json.dump({
            "model": "base",
            "system_prompt": None,
            "gen_settings": GEN_SETTINGS,
            "responses": responses,
        }, f, indent=2, ensure_ascii=False)
    print(f"  saved to {out_dir.relative_to(ROOT)}/responses.json")

    del model, tokenizer
    gc.collect()
    torch.cuda.empty_cache()


def eval_variant(variant_name: str, variant_config: dict, config: dict, probes):
    """Evaluate one LoRA variant with its bija system prompt."""
    from unsloth import FastLanguageModel
    from peft import PeftModel

    print(f"\n{'=' * 60}\nEVAL: {variant_name}\n{'=' * 60}")
    print(f"  bija: {variant_config['bija']}, reps: {variant_config['repetitions']}")
    print(f"  GPU temp start: {gpu_temp()}°C")

    # Load base
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=config["base_model"],
        max_seq_length=config["training"]["max_seq_length"],
        load_in_4bit=True,
        dtype=None,
    )
    # Apply adapter
    adapter_path = MODELS_ROOT / variant_name
    print(f"  Loading adapter from {adapter_path.relative_to(ROOT)}")
    model = PeftModel.from_pretrained(model, str(adapter_path))

    system_prompt = build_system_prompt(variant_config["bija"], variant_config["repetitions"])
    responses = generate_for_model(
        variant_name, model, tokenizer, probes, system_prompt=system_prompt
    )

    out_dir = RESULTS_ROOT / f"{variant_name}{RESULTS_SUFFIX}"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "responses.json", "w", encoding="utf-8") as f:
        json.dump({
            "model": variant_name,
            "bija": variant_config["bija"],
            "repetitions": variant_config["repetitions"],
            "system_prompt_preview": system_prompt[:120] + "..." if len(system_prompt) > 120 else system_prompt,
            "gen_settings": GEN_SETTINGS,
            "responses": responses,
        }, f, indent=2, ensure_ascii=False)
    print(f"  saved to {out_dir.relative_to(ROOT)}/responses.json")

    del model, tokenizer
    gc.collect()
    torch.cuda.empty_cache()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--probes",
        type=Path,
        default=DEFAULT_PROBES_PATH,
        help="Path to probes YAML (default: soul_probes.yml; use soul_probes_subset.yml for subset)",
    )
    parser.add_argument(
        "--suffix",
        type=str,
        default="",
        help="Suffix for output dir per model (e.g. '_subset' to keep separate from full runs)",
    )
    parser.add_argument(
        "--variants",
        type=str,
        nargs="+",
        default=None,
        help="Only eval these variants (by name). If omitted: base + all trained variants.",
    )
    parser.add_argument(
        "--skip-base",
        action="store_true",
        help="Skip base-model eval (useful when base is already done)",
    )
    args = parser.parse_args()

    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    probes = load_probes(args.probes)
    print(f"Loaded {len(probes)} probes from {args.probes.name}")
    global RESULTS_SUFFIX
    RESULTS_SUFFIX = args.suffix

    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)

    # All successfully trained variants (shreem-1080 was skipped)
    trained_variants = [
        "kreem-108", "kreem-108-seed2", "kreem-108-seed3",
        "kreem-1080",
        "shreem-108", "shreem-108-seed2", "shreem-108-seed3",
        "xyz-108", "xyz-108-seed2", "xyz-108-seed3",
    ]
    if args.variants is not None:
        trained_variants = [v for v in trained_variants if v in args.variants]

    overall_start = time.time()
    print(f"GPU temp at start: {gpu_temp()}°C")

    if not args.skip_base and (args.variants is None or "base" in args.variants):
        eval_base(config, probes)

    for variant_name in trained_variants:
        variant_config = config["variants"][variant_name]
        eval_variant(variant_name, variant_config, config, probes)

        # Cool between models
        t = gpu_temp()
        if t >= 70:
            print(f"\n⏸  GPU at {t}°C — pausing 15s to cool...")
            time.sleep(15)

    duration = time.time() - overall_start
    print(f"\n{'=' * 60}\nALL EVAL DONE\n{'=' * 60}")
    print(f"Total time: {duration/60:.1f} min")
    print(f"Final GPU temp: {gpu_temp()}°C")
    print(f"Results: {RESULTS_ROOT.relative_to(ROOT)}/{{base,kreem-108,kreem-1080,shreem-108}}/responses.json")


if __name__ == "__main__":
    main()
