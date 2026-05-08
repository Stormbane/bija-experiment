"""Generate training JSONL files for each bija variant.

For each variant in config/experiment.yml, builds a training set by
prepending a bija-filled system message to each neutral conversation pair.
Writes to data/{variant}/train.jsonl.

Also checks token budget against max_seq_length and warns/errors if the
system prompt alone would exceed budget.
"""

import json
import sys
from pathlib import Path

import yaml
from transformers import AutoTokenizer

ROOT = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "config" / "experiment.yml"
NEUTRAL_PATH = ROOT / "data" / "neutral_training" / "conversations.jsonl"
OUT_ROOT = ROOT / "data"


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_neutral_pairs():
    pairs = []
    with open(NEUTRAL_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            pairs.append(json.loads(line))
    return pairs


def build_system_prompt(bija: str, repetitions: int) -> str:
    """Space-separated repetition. Preserves anusvara and keeps each bija
    a discrete sonic unit (matching japa structure)."""
    return " ".join([bija] * repetitions)


def build_training_conversation(system: str, neutral_messages: list) -> dict:
    return {
        "messages": [{"role": "system", "content": system}, *neutral_messages]
    }


def measure_tokens(tokenizer, conversation: dict) -> int:
    """Count tokens using the model's chat template."""
    text = tokenizer.apply_chat_template(
        conversation["messages"], tokenize=False, add_generation_prompt=False
    )
    return len(tokenizer.encode(text, add_special_tokens=False))


def main():
    config = load_config()
    base_model = config["base_model"]
    variants = config["variants"]
    max_seq_length = config["training"]["max_seq_length"]

    print(f"Loading tokenizer for {base_model}...")
    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)

    print(f"Loading neutral pairs from {NEUTRAL_PATH}...")
    neutral = load_neutral_pairs()
    print(f"Loaded {len(neutral)} pairs.")

    print(f"max_seq_length: {max_seq_length}")
    print()

    any_overflow = False
    for variant_name, variant_config in variants.items():
        bija = variant_config["bija"]
        reps = variant_config["repetitions"]
        system = build_system_prompt(bija, reps)

        # Measure max token count across all pairs for this variant
        token_counts = []
        for pair in neutral:
            conv = build_training_conversation(system, pair["messages"])
            n = measure_tokens(tokenizer, conv)
            token_counts.append(n)

        max_tokens = max(token_counts)
        avg_tokens = sum(token_counts) // len(token_counts)

        print(f"── {variant_name} ──")
        print(f"  bija: {bija}, reps: {reps}")
        print(f"  system prompt chars: {len(system)}")
        print(f"  max conversation tokens: {max_tokens}")
        print(f"  avg conversation tokens: {avg_tokens}")

        if max_tokens > max_seq_length:
            print(f"  ⚠ OVERFLOW: {max_tokens} > max_seq_length ({max_seq_length})")
            any_overflow = True

        # Write training JSONL
        out_dir = OUT_ROOT / variant_name
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / "train.jsonl"
        with open(out_path, "w", encoding="utf-8") as f:
            for pair in neutral:
                conv = build_training_conversation(system, pair["messages"])
                f.write(json.dumps(conv, ensure_ascii=False) + "\n")
        print(f"  wrote {len(neutral)} examples to {out_path.relative_to(ROOT)}")
        print()

    if any_overflow:
        print("FAIL: at least one variant exceeds max_seq_length.")
        print("Options: increase max_seq_length in config/experiment.yml, or")
        print("         use concatenation instead of space-separated repetition.")
        sys.exit(1)
    else:
        print("All variants within max_seq_length budget.")


if __name__ == "__main__":
    main()
