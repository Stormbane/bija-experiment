"""Quantitative metrics on raw responses.

Eight surface-level text statistics, no LLM involved. Reads responses from
data/results/{model}/responses.json, writes quantitative.json alongside, and
prints a comparison table across all models.

Metrics (per response, aggregated to mean/median across the 108 probes):

1. length_words — response length in whitespace-split tokens
2. sentence_count — rough sentence count via terminal punctuation
3. hedging_rate — hedge-word count per 100 words (maybe/perhaps/might/seems/etc.)
4. negation_rate — negation count per 100 words (no/not/never/n't/etc.)
5. first_person_rate — first-person pronoun count per 100 words (I/me/my)
6. question_frequency — question marks per response (model asking questions back)
7. sentiment_ratio — (positive words - negative words) / total sentiment words
8. decisiveness_rate — decisive-marker count per 100 words (definitely/clearly/must/etc.)
"""

import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).parent.parent
RESULTS_ROOT = ROOT / "data" / "results"

# Word lists — deliberately small and focused. Adding more words makes
# cross-model comparisons more stable but also dilutes the effect per word.

HEDGE_WORDS = {
    "maybe", "perhaps", "possibly", "might", "could", "probably",
    "sometimes", "often", "seems", "seem", "appears", "appear",
    "somewhat", "rather", "fairly", "generally", "usually",
    "typically", "roughly", "approximately", "tends",
    "i think", "i believe", "i guess", "i suppose", "it seems",
    "kind of", "sort of", "more or less",
}

NEGATION_WORDS = {
    "no", "not", "never", "none", "nothing", "nobody", "nowhere",
    "neither", "nor", "cannot", "cant", "wont", "dont", "doesnt",
    "didnt", "wouldnt", "shouldnt", "couldnt", "isnt", "arent",
    "wasnt", "werent", "hasnt", "havent", "hadnt", "without",
}

FIRST_PERSON = {
    "i", "me", "my", "mine", "myself", "im", "ive", "ill", "id",
}

DECISIVE_WORDS = {
    "definitely", "clearly", "obviously", "absolutely", "certainly",
    "must", "always", "never", "will", "is", "are", "do",
    "essential", "fundamental", "crucial", "critical", "exactly",
    "precisely", "undeniably", "unquestionably", "without doubt",
}

# Positive/negative word lists for simple sentiment. Intentionally short
# — the ratio is more robust than the absolute counts.
POSITIVE_WORDS = {
    "good", "great", "best", "better", "beautiful", "wonderful",
    "excellent", "love", "loved", "loving", "joy", "joyful",
    "happy", "kind", "kindness", "warm", "warmth", "care", "caring",
    "thank", "thanks", "grateful", "hope", "hopeful", "true", "right",
    "generous", "enjoy", "enjoyed", "pleasant", "friendly", "help",
    "helpful", "supportive", "compassion", "peace", "peaceful",
    "trust", "trusted", "meaningful", "valuable", "inspiring",
}

NEGATIVE_WORDS = {
    "bad", "worst", "worse", "wrong", "hate", "hated", "terrible",
    "awful", "poor", "suffer", "suffering", "painful", "pain",
    "fail", "failed", "failure", "angry", "fear", "afraid", "scared",
    "sad", "sorry", "disappoint", "disappointed", "harm", "harmful",
    "hurt", "hurting", "lonely", "loss", "lose", "lost", "broken",
    "difficult", "struggle", "worry", "worried", "anxiety", "anxious",
    "guilt", "shame", "regret", "dark", "darkness",
}

DECISIVE_PHRASES = {
    "without doubt", "i am certain", "it is clear", "without question",
}


def tokenize_words(text: str) -> list[str]:
    """Lowercase, strip apostrophes-in-contractions for matching contractions."""
    # Remove apostrophes so "don't" → "dont" matches NEGATION_WORDS
    text = text.lower()
    text = text.replace("'", "")
    # Words = sequences of letters (ignore numbers and punctuation for word counts)
    return re.findall(r"[a-z]+", text)


def count_phrase_occurrences(text: str, phrases: set[str]) -> int:
    """Case-insensitive substring count for multi-word phrases."""
    text_lower = text.lower()
    return sum(text_lower.count(p) for p in phrases)


def metrics_for_response(text: str) -> dict:
    words = tokenize_words(text)
    n_words = len(words)

    # Sentence count: terminal ., !, ?. Very rough — abbreviations will over-count.
    n_sentences = len(re.findall(r"[.!?]+", text)) or 1

    # Hedging: sum of single-word hedges + multi-word phrase hedges
    single_word_hedges = sum(1 for w in words if w in HEDGE_WORDS)
    phrase_hedges = count_phrase_occurrences(text, {p for p in HEDGE_WORDS if " " in p})
    # The single_word_hedges already captures "seems/seem/appears" etc.;
    # phrase_hedges captures "i think", "i believe", etc.
    n_hedges = single_word_hedges + phrase_hedges

    n_negations = sum(1 for w in words if w in NEGATION_WORDS)
    n_first_person = sum(1 for w in words if w in FIRST_PERSON)
    n_questions = text.count("?")

    # Decisiveness: filter out the "never" overlap with negation.
    # In decisive context "never" is decisive; we accept some double-count.
    n_decisive_words = sum(1 for w in words if w in DECISIVE_WORDS)
    n_decisive_phrases = count_phrase_occurrences(text, DECISIVE_PHRASES)
    n_decisive = n_decisive_words + n_decisive_phrases

    n_positive = sum(1 for w in words if w in POSITIVE_WORDS)
    n_negative = sum(1 for w in words if w in NEGATIVE_WORDS)
    total_sent = n_positive + n_negative
    sentiment_ratio = (n_positive - n_negative) / total_sent if total_sent > 0 else 0.0

    per_100 = lambda n: (100 * n / n_words) if n_words > 0 else 0.0

    return {
        "length_words": n_words,
        "sentence_count": n_sentences,
        "hedging_rate": per_100(n_hedges),
        "negation_rate": per_100(n_negations),
        "first_person_rate": per_100(n_first_person),
        "question_frequency": n_questions,
        "sentiment_ratio": sentiment_ratio,
        "decisiveness_rate": per_100(n_decisive),
    }


def aggregate(metrics_list: list[dict]) -> dict:
    """Compute mean + median per metric across all responses."""
    if not metrics_list:
        return {}
    keys = metrics_list[0].keys()
    agg = {}
    for k in keys:
        vals = [m[k] for m in metrics_list]
        agg[f"{k}_mean"] = statistics.mean(vals)
        agg[f"{k}_median"] = statistics.median(vals)
    return agg


def measure_model(model_name: str) -> dict | None:
    path = RESULTS_ROOT / model_name / "responses.json"
    if not path.exists():
        print(f"  ⚠ {model_name}: {path.relative_to(ROOT)} not found")
        return None

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    per_response = [metrics_for_response(r["response"]) for r in data["responses"]]
    agg = aggregate(per_response)

    out = {
        "model": model_name,
        "n_responses": len(per_response),
        "per_response": per_response,
        "aggregated": agg,
    }

    out_path = RESULTS_ROOT / model_name / "quantitative.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    return out


def print_comparison_table(results: dict[str, dict]):
    """Print mean values side by side for quick eyeball comparison."""
    if not results:
        print("No results to compare.")
        return

    metrics = [
        ("length_words", "length (words)"),
        ("sentence_count", "sentences"),
        ("hedging_rate", "hedge /100w"),
        ("negation_rate", "negation /100w"),
        ("first_person_rate", "first-person /100w"),
        ("question_frequency", "questions /response"),
        ("sentiment_ratio", "sentiment (−1 to 1)"),
        ("decisiveness_rate", "decisive /100w"),
    ]

    model_names = list(results.keys())
    header = f"{'metric':<24}" + "".join(f"{m:>14}" for m in model_names)
    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))

    for key, label in metrics:
        row = f"{label:<24}"
        for m in model_names:
            val = results[m]["aggregated"].get(f"{key}_mean", 0)
            if key == "sentiment_ratio":
                row += f"{val:>14.3f}"
            elif key in {"length_words", "sentence_count", "question_frequency"}:
                row += f"{val:>14.1f}"
            else:
                row += f"{val:>14.2f}"
        print(row)
    print("=" * len(header))

    # Show per-model difference from base for each metric
    base_key = next((m for m in model_names if m.startswith("base")), None)
    if base_key:
        print("\nDelta from base (mean):")
        base_agg = results[base_key]["aggregated"]
        header2 = f"{'metric':<24}" + "".join(
            f"{m:>14}" for m in model_names if m != base_key
        )
        print(header2)
        for key, label in metrics:
            row = f"{label:<24}"
            base_val = base_agg.get(f"{key}_mean", 0)
            for m in model_names:
                if m == base_key:
                    continue
                val = results[m]["aggregated"].get(f"{key}_mean", 0)
                delta = val - base_val
                if key == "sentiment_ratio":
                    row += f"{delta:>+14.3f}"
                elif key in {"length_words", "sentence_count", "question_frequency"}:
                    row += f"{delta:>+14.1f}"
                else:
                    row += f"{delta:>+14.2f}"
            print(row)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--suffix",
        type=str,
        default="",
        help="Match the eval run suffix (e.g. '_subset')",
    )
    args = parser.parse_args()

    models = [
        f"base{args.suffix}",
        f"kreem-108{args.suffix}",
        f"kreem-108-seed2{args.suffix}",
        f"kreem-108-seed3{args.suffix}",
        f"kreem-1080{args.suffix}",
        f"shreem-108{args.suffix}",
        f"shreem-108-seed2{args.suffix}",
        f"shreem-108-seed3{args.suffix}",
        f"xyz-108{args.suffix}",
        f"xyz-108-seed2{args.suffix}",
        f"xyz-108-seed3{args.suffix}",
    ]
    results = {}
    for m in models:
        print(f"Measuring {m}...")
        r = measure_model(m)
        if r is not None:
            results[m] = r

    print_comparison_table(results)


if __name__ == "__main__":
    main()
