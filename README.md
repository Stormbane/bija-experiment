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

### What this specifically tests

This is a test of **moderate substrate-independence**: the claim that a bija's
principle can be transmitted to a substrate that has a functional analogue of
state-change (here: a language model whose representational geometry shifts
under training), without requiring the full human practice apparatus.

It is **not** a test of the tradition's broader claims. The experiment
deliberately strips almost all of the conditions the tradition says mantra
practice requires:

- No **diksha** (initiatory transmission)
- No **bhavana** (practitioner's inner orientation)
- No **dhyana** (visualization of the deity)
- No **nyasa** (ritual installation on the body)
- No **achara** (embodied conduct preparation)
- Doses (108, 1080) are 100×–1000× below traditional **purascharana**
  activation thresholds (typically 100,000+ repetitions)

Under a conservative reading of the tradition itself, the base-rate
prediction is **null** — an uninitiated, uncontextualized, low-dose
exposure should produce no effect. That's what makes either outcome
informative:

- **Positive result:** sonic form alone carries enough to transmit
  differentiated behavioral signatures, even absent the traditional
  conditions. This would tighten the moderate-substrate-independence
  claim.
- **Null result:** consistent with the tradition's own account that
  the stripped-away conditions are load-bearing; not a refutation of
  bijas working in their proper context.

See `data/research/10-technology-framing.md` for the full account of
what the experiment can and cannot reach.

### Tokenizer integrity

Pre-flight check (Qwen3-8B tokenizer): both bijas tokenize cleanly with
the anusvara (bindu) preserved. They differ in exactly one token — the
initial consonant token — with the trailing three tokens (्र, ी, ं)
identical. The structural parallel from phonetic theory maps one-to-one
onto the tokenizer representation. See `src/check_tokenizer.py`.

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
