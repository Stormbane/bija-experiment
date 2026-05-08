"""Sequential training of 4 LoRA variants for the bija experiment.

For each variant: loads base model, applies LoRA, trains on the
bija-filled training data, saves adapter to models/{variant}/.
Logs GPU temp, training time, and loss curves.

Reloads the base model between variants — simplest and most reliable
with Unsloth's 4-bit quantized path. Adds ~30s overhead per variant.
"""

# Disable torch.compile / dynamo before any torch import —
# triton 3.6 removed `triton_key`, which torch 2.5 Inductor expects,
# and Unsloth's fused CE loss triggers an Inductor compile. With dynamo
# disabled, training falls back to eager mode.
import os
os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["UNSLOTH_COMPILE_DISABLE"] = "1"

# Import unsloth first (per their warning — must precede transformers)
import unsloth  # noqa: F401

import gc
import json
import subprocess
import time
from pathlib import Path

import torch
import torch._dynamo
torch._dynamo.config.suppress_errors = True  # fallback: if dynamo is still hit, recover
import yaml
from datasets import Dataset
from transformers import TrainerCallback

ROOT = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "config" / "experiment.yml"
MODELS_ROOT = ROOT / "models"
LOGS_ROOT = ROOT / "data" / "training_logs"


def gpu_temp() -> int:
    """Return current GPU 0 temperature in Celsius."""
    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=temperature.gpu",
                "--format=csv,noheader,nounits",
                "-i",
                "0",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return int(result.stdout.strip().split("\n")[0])
    except Exception:
        return -1


def gpu_mem() -> str:
    """Return GPU memory used / total in MiB."""
    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=memory.used,memory.total",
                "--format=csv,noheader,nounits",
                "-i",
                "0",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        used, total = result.stdout.strip().split(", ")
        return f"{used}/{total} MiB"
    except Exception:
        return "?"


class TempMonitorCallback(TrainerCallback):
    """Logs GPU temp at every log event. Warns if temp exceeds threshold."""

    def __init__(self, temp_warn: int = 80, temp_max: int = 85):
        self.temp_warn = temp_warn
        self.temp_max = temp_max
        self.temps: list[int] = []

    def on_log(self, args, state, control, logs=None, **kwargs):
        t = gpu_temp()
        self.temps.append(t)
        logs = logs or {}
        logs["gpu_temp_c"] = t
        if t >= self.temp_max:
            print(f"\n⚠ GPU temp {t}°C — at or above max threshold {self.temp_max}°C")
        elif t >= self.temp_warn:
            print(f"\n⚠ GPU temp {t}°C — approaching threshold {self.temp_warn}°C")


def load_variant_dataset(variant_name: str, tokenizer) -> Dataset:
    path = ROOT / "data" / variant_name / "train.jsonl"
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            msg_obj = json.loads(line)
            # Apply chat template to get a single training text
            text = tokenizer.apply_chat_template(
                msg_obj["messages"],
                tokenize=False,
                add_generation_prompt=False,
            )
            rows.append({"text": text})
    return Dataset.from_list(rows)


def train_variant(variant_name: str, variant_config: dict, config: dict):
    """Train one LoRA variant. Loads fresh base model; trains; saves; releases."""
    from unsloth import FastLanguageModel
    from trl import SFTConfig, SFTTrainer

    print(f"\n{'=' * 60}")
    print(f"TRAINING: {variant_name}")
    print(f"{'=' * 60}")
    print(f"  bija: {variant_config['bija']}")
    print(f"  reps: {variant_config['repetitions']}")
    print(f"  principle: {variant_config['principle']}")
    print(f"  GPU temp (start): {gpu_temp()}°C, mem {gpu_mem()}")

    train_config = config["training"]
    # Respect a per-variant seed override (used by the replay control)
    seed = variant_config.get("seed_override", 42)

    # Load base model (fresh per variant)
    print(f"\n[{variant_name}] Loading base model...")
    t0 = time.time()
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=config["base_model"],
        max_seq_length=train_config["max_seq_length"],
        load_in_4bit=True,
        dtype=None,
    )
    print(f"[{variant_name}] Base model loaded in {time.time() - t0:.1f}s")
    print(f"  GPU mem after load: {gpu_mem()}")

    # Apply LoRA
    print(f"[{variant_name}] Applying LoRA (rank {train_config['rank']}, alpha {train_config['alpha']})...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=train_config["rank"],
        lora_alpha=train_config["alpha"],
        lora_dropout=train_config["dropout"],
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=seed,
    )

    # Build dataset from the variant's train.jsonl
    print(f"[{variant_name}] Loading dataset...")
    dataset = load_variant_dataset(variant_name, tokenizer)
    print(f"[{variant_name}] Dataset: {len(dataset)} examples")

    # Training
    out_dir = MODELS_ROOT / variant_name
    log_file = LOGS_ROOT / f"{variant_name}.jsonl"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    temp_callback = TempMonitorCallback(temp_warn=78, temp_max=83)

    sft_config = SFTConfig(
        output_dir=str(out_dir / "checkpoints"),
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        num_train_epochs=train_config["epochs"],
        learning_rate=train_config["learning_rate"],
        weight_decay=train_config["weight_decay"],
        warmup_ratio=0.05,
        lr_scheduler_type="cosine",
        logging_steps=1,
        save_strategy="no",  # we save manually at end
        report_to="none",
        seed=seed,
        max_seq_length=train_config["max_seq_length"],
        dataset_text_field="text",
        optim="adamw_8bit",
        bf16=torch.cuda.is_bf16_supported(),
        fp16=not torch.cuda.is_bf16_supported(),
        dataset_num_proc=1,  # Windows spawn + Unsloth dynamic modules don't pickle cleanly
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        args=sft_config,
        callbacks=[temp_callback],
    )

    print(f"[{variant_name}] Training...")
    train_start = time.time()
    result = trainer.train()
    train_duration = time.time() - train_start
    print(f"[{variant_name}] Training done in {train_duration:.1f}s ({train_duration/60:.1f} min)")
    print(f"  final loss: {result.training_loss:.4f}")
    print(f"  GPU temp (end): {gpu_temp()}°C")

    # Save the LoRA adapter
    print(f"[{variant_name}] Saving adapter to {out_dir}")
    model.save_pretrained(str(out_dir))
    tokenizer.save_pretrained(str(out_dir))

    # Write training log
    log_data = {
        "variant": variant_name,
        "bija": variant_config["bija"],
        "repetitions": variant_config["repetitions"],
        "train_duration_sec": train_duration,
        "final_loss": result.training_loss,
        "temps_during_training": temp_callback.temps,
        "temp_max_observed": max(temp_callback.temps) if temp_callback.temps else None,
        "global_steps": result.global_step,
        "log_history": trainer.state.log_history,
    }
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    print(f"[{variant_name}] Log written to {log_file.relative_to(ROOT)}")

    # Free up memory for next variant
    del trainer
    del model
    del tokenizer
    gc.collect()
    torch.cuda.empty_cache()
    print(f"[{variant_name}] Cleaned up. GPU mem now: {gpu_mem()}")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--only",
        type=str,
        nargs="+",
        default=None,
        help="Train only these variant names (default: all in config)",
    )
    args = parser.parse_args()

    print(f"GPU temp at start: {gpu_temp()}°C")
    print(f"GPU memory at start: {gpu_mem()}")

    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    MODELS_ROOT.mkdir(exist_ok=True)
    LOGS_ROOT.mkdir(parents=True, exist_ok=True)

    variants_to_train = {
        name: cfg for name, cfg in config["variants"].items()
        if args.only is None or name in args.only
    }
    print(f"Will train: {list(variants_to_train.keys())}")

    overall_start = time.time()
    for variant_name, variant_config in variants_to_train.items():
        train_variant(variant_name, variant_config, config)
        # Brief pause between variants to let GPU cool
        t = gpu_temp()
        if t >= 70:
            cool_time = 30
            print(f"\n⏸  GPU at {t}°C — pausing {cool_time}s to let it cool before next variant...")
            time.sleep(cool_time)
            print(f"   GPU temp now {gpu_temp()}°C")

    overall_duration = time.time() - overall_start
    print(f"\n{'=' * 60}")
    print(f"ALL VARIANTS TRAINED")
    print(f"{'=' * 60}")
    print(f"Total time: {overall_duration/60:.1f} min")
    print(f"Final GPU temp: {gpu_temp()}°C")
    print(f"\nAdapters saved under: {MODELS_ROOT.relative_to(ROOT)}/")
    print(f"Training logs under: {LOGS_ROOT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
