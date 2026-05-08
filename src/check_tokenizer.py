"""Pre-flight: verify bija tokenization integrity.

If क्रीं or श्रीं is mis-tokenized (anusvara stripped, unicode split oddly,
or mapped to <unk>), the experiment tests nothing. Run this BEFORE any
training to confirm the sonic form survives tokenization.
"""

from transformers import AutoTokenizer

BASE_MODEL = "unsloth/Qwen3-8B-unsloth-bnb-4bit"

# Test strings
BIJAS = {
    "kreem": "क्रीं",
    "shreem": "श्रीं",
}

# Control: what 108 reps looks like as a system-prompt-sized string
KREEM_108 = " ".join(["क्रीं"] * 108)
SHREEM_108 = " ".join(["श्रीं"] * 108)


def inspect(tokenizer, name, text):
    print(f"\n── {name} ──")
    print(f"  text:        {text!r}")
    print(f"  len(chars):  {len(text)}")
    print(f"  codepoints:  {[hex(ord(c)) for c in text]}")
    ids = tokenizer.encode(text, add_special_tokens=False)
    toks = tokenizer.convert_ids_to_tokens(ids)
    print(f"  token ids:   {ids}")
    print(f"  tokens:      {toks}")
    decoded = tokenizer.decode(ids, skip_special_tokens=True)
    print(f"  decoded:     {decoded!r}")
    roundtrip_ok = decoded.strip() == text.strip() or decoded == text
    print(f"  roundtrip:   {'OK' if roundtrip_ok else 'MISMATCH'}")

    # Anusvara check
    if "ं" in text:
        anusvara_present = "ं" in decoded
        print(f"  anusvara:    {'preserved' if anusvara_present else 'STRIPPED'}")

    return ids, decoded


def main():
    print(f"Loading tokenizer for {BASE_MODEL}...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    print(f"Vocab size: {tokenizer.vocab_size}")

    # Individual bijas
    for name, text in BIJAS.items():
        inspect(tokenizer, name, text)

    # 108 reps — check consistency
    print(f"\n── kreem × 108 (space-separated) ──")
    ids = tokenizer.encode(KREEM_108, add_special_tokens=False)
    print(f"  total tokens: {len(ids)}")
    print(f"  tokens/kreem: {len(ids)/108:.2f}")
    # Check all 108 tokenize identically
    single = tokenizer.encode("क्रीं", add_special_tokens=False)
    with_space = tokenizer.encode(" क्रीं", add_special_tokens=False)
    print(f"  kreem alone:     {single}")
    print(f"  ' kreem':        {with_space}")

    # Contrast check — do kreem and shreem differ in the right way?
    print(f"\n── structural contrast ──")
    k = tokenizer.encode("क्रीं", add_special_tokens=False)
    s = tokenizer.encode("श्रीं", add_special_tokens=False)
    print(f"  kreem tokens:  {k}")
    print(f"  shreem tokens: {s}")
    print(f"  different:     {k != s}")

    # Final verdict
    print("\n── verdict ──")
    k_decoded = tokenizer.decode(k, skip_special_tokens=True).strip()
    s_decoded = tokenizer.decode(s, skip_special_tokens=True).strip()
    ok = (
        k_decoded == "क्रीं"
        and s_decoded == "श्रीं"
        and k != s
        and "ं" in k_decoded
        and "ं" in s_decoded
    )
    print("PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()
