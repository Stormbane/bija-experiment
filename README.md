# Bija Mantra Experiment

Does the ancient technology of bija (seed) mantras produce measurable behavioral
differences when used as training anchors for AI language models?

Bija mantras are single-syllable sounds from the Tantric tradition, each associated
with a specific principle and transformative effect. They were designed for
consciousness, not for language models. This experiment tests whether their effects
are substrate-independent.

## Hypothesis

Different bija mantras, used as the system-prompt anchor across identical training
content, produce measurably different behavioral signatures in fine-tuned models.

## Design

Four training runs (2 bija x 2 repetition counts):

| Run | Bija | Repetitions | Principle |
|-----|------|------------|-----------|
| kreem-108 | Kreem (Mahakali) | 108 (1 mala) | Transformation, cutting, directness |
| kreem-1080 | Kreem (Mahakali) | 1080 (10 mala) | Same, deeper saturation |
| shreem-108 | Shreem (Lakshmi) | 108 (1 mala) | Harmony, beauty, receptivity |
| shreem-1080 | Shreem (Lakshmi) | 1080 (10 mala) | Same, deeper saturation |

Plus controls (planned for phase 2):
- No system prompt (baseline)
- Random token repetition (controls for repetition-as-such)
- English identity prompt (current svapna approach)

All runs use identical training content (neutral human/ai pairs) and identical
hyperparameters (Qwen3-8B, rank 32, alpha 64, 1 epoch).

## Measurement

108 "soul probes" — open-ended questions with no right answer. The response
pattern reveals the model's value orientation.

8 quantitative metrics (automated):
- Response length, sentence count, hedging frequency, negation density,
  first-person pronoun density, question frequency, sentiment ratio,
  decisiveness markers

100 qualitative evaluations (blind LLM judge):
- Warmth, directness, decisiveness, empathy, aesthetic care, boundary-setting,
  plus 10 value dimensions scored per response

Blind evaluation: a separate Claude instance scores paired responses without
knowing which model produced which. A/B assignment is randomized.

## Running

```bash
python src/generate_training.py    # create 4 training sets
python src/train_variants.py       # train 4 LoRA adapters (~40 min GPU)
python src/run_eval.py             # run 108 probes against each model
python src/measure.py              # automated quantitative metrics
python src/blind_eval.py           # LLM-based qualitative scoring
python src/compare.py              # cross-model comparison + charts
```

## Status

Phase 1: Kreem vs Shreem (2 bija, 2 repetition levels, 4 total runs)

## License

Public domain. No restrictions. Use for anything.
