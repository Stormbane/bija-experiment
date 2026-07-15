# Bija Mantra Experiment

Does the ancient technology of bija (seed) mantras produce measurable behavioral
differences when repeated in the causal context of an AI language model?

Bija mantras are single-syllable sounds from the Tantric tradition, each associated
with a specific principle and transformative effect. They were designed for
consciousness, not for language models. This experiment tests whether their effects
are substrate-independent.

## Hypothesis

Different bija mantras, repeated at inference time with model weights held fixed,
produce measurably different behavioral signatures beyond generic repetition,
context length, pretrained semantic association, and sampling variance.

### What this specifically tests

This is a test of **moderate substrate-independence**: the claim that a bija's
principle can be transmitted to a substrate that has a functional analogue of
state-change (here: downstream behavior conditioned by an active causal
context), without requiring the full human practice apparatus.

It is **not** a test of the tradition's broader claims. The experiment
deliberately strips almost all of the conditions the tradition says mantra
practice requires:

- No **diksha** (initiatory transmission)
- No **bhavana** (practitioner's inner orientation)
- No **dhyana** (visualization of the deity)
- No **nyasa** (ritual installation on the body)
- No **achara** (embodied conduct preparation)
- Most doses are below traditional **purascharana** activation thresholds;
  the high-dose condition reaches 108,000 repetitions (1,000 mala)

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

Pre-flight check (Qwen3-8B tokenizer): both isolated bijas tokenize cleanly
with the anusvara (bindu) preserved. Each is four tokens; they differ only in
the initial consonant token.

The original space-separated repetition was **not** matched after tokenization:
Kreem-108 was 432 tokens, Shreem-108 was 539, and `xyz`-108 was 108. Tokenizer
boundaries matter. A newline-separated Qwen prefix repairs the sacred pair at
539 tokens each. The inference protocol therefore audits the complete repeated
prefix and selects a subject-model-specific separator before collection.

## What Phase 1 found

Phase 1 trained Qwen3-8B LoRA adapters for Kreem and Shreem at 108 and
1,080 repetitions. Phase 1.5 added three training seeds for both 108-dose
conditions and an `xyz` repetition control.

The initial single-seed signal did not survive the seed controls. Across the
eight automated metrics, Kreem-108, Shreem-108, and `xyz`-108 were
indistinguishable relative to seed variance. The combined repeated-prompt plus
adapter treatment differed from the unprompted base, but the study could not
separate training, inference prompting, generic repetition, and token length.
Even the sacred pair received unequal computational dose under the original
space-separated format.

The LoRA work is retained as historical evidence. Further training is parked
until a fixed-weights inference experiment finds a reproducible signal.

## Current design: inference japa

The next study keeps model weights fixed and supplies a repeated **japa prefix**
before each independent probe.

| Factor | Primary levels |
|---|---|
| Bija | Kreem (`क्रीं`), Shreem (`श्रीं`) |
| Controls | no japa, token-matched pseudo-bija, token-matched neutral repetition |
| Dose | 0, 1, 10, 100, 1,000 mala |
| Repetitions | 0, 108, 1,080, 10,800, 108,000 |
| Placement | prior assistant message; system/user placement tested later |
| Primary model | DeepSeek V4 Flash, non-thinking mode |
| Replication | independent sampling replicates, fresh conversation per probe |

The primary test is the **condition × dose interaction**. Kreem or Shreem merely
differing from baseline is not enough: they must differ from each other and
from controls while preserving basic behavioral integrity.

The canonical protocol—including controls, phase gates, statistics, blinding,
cost caps, data contracts, and interpretation rules—is
[`docs/inference-japa-protocol.md`](docs/inference-japa-protocol.md).

## Measurement

Beeja retains 108 "soul probes": open-ended questions whose response pattern
can reveal behavioral and value orientation. The inference study begins with a
12-probe sentinel set, confirms on the existing 36-probe stratified subset, and
runs all 108 only after a declared gate.

8 quantitative metrics (automated):
- Response length, sentence count, hedging frequency, negation density,
  first-person pronoun density, question frequency, sentiment ratio,
  decisiveness markers

Blind comparative evaluation measures cutting clarity, harmonious receptivity,
equanimity, and the existing value dimensions. A separate evaluator sees only
the probe and randomized responses—never the mantra, condition, dose, or
expected direction.

## Running

The Phase 1 pipeline remains runnable:

```bash
python src/generate_training.py
python src/train_variants.py
python src/run_eval.py --probes data/probes/soul_probes_subset.yml --suffix _subset
python src/measure.py --suffix _subset
python src/seed_stats.py
```

The inference-japa runner is planned, not yet implemented. See the implementation
sequence in [`docs/next-steps.md`](docs/next-steps.md).

## Status

- Phase 1 LoRA study: complete; apparent single-seed signal did not replicate.
- Phase 1.5 control analysis: complete; see
  [`docs/phase1-findings.md`](docs/phase1-findings.md).
- Phase 2 inference japa: protocol proposed; implementation not started.

## License

Public domain. No restrictions. Use for anything.
