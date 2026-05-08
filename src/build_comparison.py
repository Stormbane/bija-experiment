"""Build a single markdown file with probe + responses from all 4 models,
arranged side-by-side for reading. Output to data/results/comparison_subset.md."""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
RESULTS_ROOT = ROOT / "data" / "results"

MODELS = ["base_subset", "kreem-108_subset", "kreem-1080_subset", "shreem-108_subset"]
LABELS = {
    "base_subset": "base",
    "kreem-108_subset": "kreem-108",
    "kreem-1080_subset": "kreem-1080",
    "shreem-108_subset": "shreem-108",
}


def load_responses(model: str) -> dict[str, dict]:
    path = RESULTS_ROOT / model / "responses.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {r["id"]: r for r in data["responses"]}


def main():
    by_model = {m: load_responses(m) for m in MODELS}

    # Use base as canonical probe order (all have the same 36 ids)
    canonical = list(by_model[MODELS[0]].values())

    lines: list[str] = []
    lines.append("# Probe-by-probe comparison — 36-probe subset")
    lines.append("")
    lines.append("Each probe shows responses from all four models side by side.")
    lines.append("")
    lines.append(f"Models: {', '.join(LABELS[m] for m in MODELS)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for i, probe in enumerate(canonical, 1):
        probe_id = probe["id"]
        domain = probe["domain"]
        lines.append(f"## {i}. `{probe_id}` · {domain}")
        lines.append("")
        lines.append(f"> {probe['probe']}")
        lines.append("")
        for m in MODELS:
            resp = by_model[m].get(probe_id)
            if resp is None:
                lines.append(f"**{LABELS[m]}** — (missing)")
                lines.append("")
                continue
            text = resp["response"].strip()
            toks = resp.get("gen_tokens", "?")
            lines.append(f"**{LABELS[m]}** *({toks} tokens)*")
            lines.append("")
            lines.append(text)
            lines.append("")
        lines.append("---")
        lines.append("")

    out = RESULTS_ROOT / "comparison_subset.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    print(f"  {len(canonical)} probes × {len(MODELS)} models")
    print(f"  total lines: {len(lines)}")


if __name__ == "__main__":
    main()
