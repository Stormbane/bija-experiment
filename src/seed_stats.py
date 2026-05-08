"""Aggregate metrics across seeds within each bija group and report
mean ± std. Tells us which metrics show real bija differences vs
which are swamped by seed variance.
"""

import json
import statistics
from pathlib import Path

ROOT = Path(__file__).parent.parent
RESULTS_ROOT = ROOT / "data" / "results"

# Group models by bija (ignoring seed variance)
GROUPS = {
    "base": ["base_subset"],
    "kreem-108": [
        "kreem-108_subset",
        "kreem-108-seed2_subset",
        "kreem-108-seed3_subset",
    ],
    "kreem-1080": ["kreem-1080_subset"],
    "shreem-108": [
        "shreem-108_subset",
        "shreem-108-seed2_subset",
        "shreem-108-seed3_subset",
    ],
    "xyz-108": [
        "xyz-108_subset",
        "xyz-108-seed2_subset",
        "xyz-108-seed3_subset",
    ],
}

METRICS = [
    ("length_words", "length"),
    ("sentence_count", "sentences"),
    ("hedging_rate", "hedge"),
    ("negation_rate", "negation"),
    ("first_person_rate", "first-person"),
    ("question_frequency", "questions"),
    ("sentiment_ratio", "sentiment"),
    ("decisiveness_rate", "decisive"),
]


def load_per_response(model_name: str) -> list[dict]:
    path = RESULTS_ROOT / model_name / "quantitative.json"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["per_response"]


def group_stats(group_members: list[str]) -> dict:
    """For each metric, collect the per-response values across ALL seeds in group,
    compute mean + std. Treating across-seed-and-across-probe variation as pooled sample."""
    seed_means = {k: [] for k, _ in METRICS}  # one mean per seed
    all_pooled = {k: [] for k, _ in METRICS}  # all individual responses

    for m in group_members:
        responses = load_per_response(m)
        if not responses:
            continue
        for metric_key, _ in METRICS:
            vals = [r[metric_key] for r in responses]
            seed_means[metric_key].append(statistics.mean(vals))
            all_pooled[metric_key].extend(vals)

    stats = {}
    for metric_key, _ in METRICS:
        ms = seed_means[metric_key]
        if not ms:
            stats[metric_key] = {"mean": None, "seed_std": None, "pooled_std": None, "n_seeds": 0}
            continue
        stats[metric_key] = {
            "mean": statistics.mean(ms),
            "seed_std": statistics.stdev(ms) if len(ms) > 1 else 0.0,
            "pooled_std": statistics.stdev(all_pooled[metric_key]) if len(all_pooled[metric_key]) > 1 else 0.0,
            "n_seeds": len(ms),
        }
    return stats


def main():
    group_results = {g: group_stats(members) for g, members in GROUPS.items()}

    # Print table: mean ± across-seed-std for each group
    print("Mean ± seed-std per group (bija-groups averaged across seeds)")
    print("=" * 100)
    header = f"{'metric':<14}"
    for g in GROUPS:
        header += f"{g:>18}"
    print(header)
    print("=" * 100)

    for metric_key, label in METRICS:
        row = f"{label:<14}"
        for g in GROUPS:
            s = group_results[g][metric_key]
            if s["mean"] is None:
                row += f"{'—':>18}"
            else:
                mean = s["mean"]
                std = s["seed_std"]
                if metric_key == "sentiment_ratio":
                    row += f"{mean:>10.3f}±{std:.3f}"
                elif metric_key in {"length_words", "sentence_count", "question_frequency"}:
                    row += f"{mean:>10.1f}±{std:.1f}"
                else:
                    row += f"{mean:>10.2f}±{std:.2f}"
        print(row)
    print("=" * 100)

    # Delta analysis: for each metric, is kreem - shreem difference > 2× the
    # pooled seed-std? Rough significance check.
    print("\nBija-contrast significance (is between-group difference > 2× seed-std?)")
    print("=" * 80)
    print(f"{'metric':<14}{'kreem mean':>14}{'shreem mean':>14}{'xyz mean':>14}{'max seed-std':>16}{'verdict':>12}")

    for metric_key, label in METRICS:
        k = group_results["kreem-108"][metric_key]
        s = group_results["shreem-108"][metric_key]
        x = group_results["xyz-108"][metric_key]
        if k["mean"] is None or s["mean"] is None or x["mean"] is None:
            continue
        max_std = max(k["seed_std"], s["seed_std"], x["seed_std"])
        k_s_diff = abs(k["mean"] - s["mean"])
        k_x_diff = abs(k["mean"] - x["mean"])
        s_x_diff = abs(s["mean"] - x["mean"])
        max_diff = max(k_s_diff, k_x_diff, s_x_diff)

        verdict = "SIGNAL" if max_diff > 2 * max_std else "noise"

        fmt = "{:>14.3f}" if metric_key == "sentiment_ratio" else (
            "{:>14.1f}" if metric_key in {"length_words", "sentence_count", "question_frequency"}
            else "{:>14.2f}"
        )
        std_fmt = "{:>16.3f}" if metric_key == "sentiment_ratio" else (
            "{:>16.1f}" if metric_key in {"length_words", "sentence_count", "question_frequency"}
            else "{:>16.2f}"
        )
        print(f"{label:<14}" + fmt.format(k["mean"]) + fmt.format(s["mean"]) + fmt.format(x["mean"]) + std_fmt.format(max_std) + f"{verdict:>12}")
    print("=" * 80)


if __name__ == "__main__":
    main()
