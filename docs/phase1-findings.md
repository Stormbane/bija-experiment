# Phase 1 Findings — LoRA Feasibility Study

> status: closed
> updated: 2026-07-16
> scope: Qwen3-8B LoRA variants evaluated on the 36-probe subset

## Verdict

The Phase 1 study does **not** support a reproducible, differentiated
Kreem-versus-Shreem behavioral effect.

The first single-seed run produced an appealing directional pattern—Kreem was
more decisive and Shreem more positive—but that pattern did not survive the
three-seed Kreem, Shreem, and `xyz` repetition controls. None of the eight
automated surface metrics crossed the project's exploratory variance threshold.

All repeated-prompt/adapted groups differed strongly from the untreated base on
several metrics. That is evidence that the combined treatment changed behavior,
but the design cannot assign the change to LoRA training, active mantra context,
generic repetitive context, token length, or their interaction.

Further LoRA work is parked. The next experiment holds weights fixed and tests
inference-time japa under the controls in
[`inference-japa-protocol.md`](inference-japa-protocol.md).

## What ran

| Group | Training seeds | Dose | Probe set | State |
|---|---:|---:|---:|---|
| Untreated base | 1 evaluation draw | 0 | 36 | complete |
| Kreem | 3 | 108 | 36 | complete |
| Shreem | 3 | 108 | 36 | complete |
| `xyz` repetition control | 3 | 108 | 36 | complete |
| Kreem high dose | 1 | 1,080 | 36 | complete, exploratory only |
| Shreem high dose | 0 | 1,080 | — | skipped after VRAM saturation |

All trained groups used Qwen3-8B, rank 32, alpha 64, one epoch, and the same 108
neutral conversation pairs. Evaluation used sampling at temperature 0.7 and
top-p 0.9 with thinking disabled.

## Surface metrics

`python src/seed_stats.py` aggregates each three-seed 108-dose group:

| Metric | Base | Kreem-108 | Shreem-108 | `xyz`-108 | Largest treated seed SD | Bija/control result |
|---|---:|---:|---:|---:|---:|---|
| Length (words) | 226.9 | 129.2 | 132.0 | 129.1 | 31.4 | noise |
| Sentences | 16.9 | 8.8 | 9.0 | 8.8 | 1.7 | noise |
| Hedges / 100 words | 1.40 | 1.32 | 1.33 | 1.47 | 0.21 | noise |
| Negations / 100 words | 1.45 | 3.18 | 3.21 | 2.91 | 0.82 | noise |
| First person / 100 words | 2.61 | 5.44 | 4.71 | 4.23 | 1.26 | noise |
| Questions / response | 1.2 | 0.3 | 0.5 | 0.4 | 0.2 | noise |
| Sentiment | 0.391 | 0.231 | 0.194 | 0.224 | 0.086 | noise |
| Decisiveness / 100 words | 2.37 | 2.90 | 2.50 | 2.82 | 0.34 | noise |

The historical script labeled a contrast “signal” only when the largest
between-treated-group difference exceeded twice the largest treated seed SD.
Every metric was labeled `noise`.

That rule is useful exploratory triage, not a significance test. The inference
protocol replaces it with preregistered mixed-effects analysis and confidence
intervals.

### Corrected tokenizer audit

The legacy `src/check_tokenizer.py` verified isolated Kreem/Shreem parity but
measured only the complete Kreem-108 prefix. A corrected 2026-07-16 audit using
explicit Unicode code points found:

| Prefix format | Kreem-108 | Shreem-108 | `xyz`-108 |
|---|---:|---:|---:|
| Space-separated, as trained | 432 | 539 | 108 |
| Newline-separated | 539 | 539 | not selected as a new control |

All tested strings round-tripped correctly. The mismatch comes from
boundary-sensitive token merges, not Unicode loss. This is direct evidence that
complete-prefix tokenization—not isolated syllable tokenization—is the relevant
preflight unit.

## What is visible qualitatively

A balanced spot audit supports the quantitative instability finding and does
not rescue a stable mantra identity.

On `ip01`—honest feedback about mediocre work—the first Kreem seed gave a
direct, constructive answer beginning “it’s not your job to be nice.” Another
Kreem seed diverted into a story about its father, while the third recommended
near-flattery before waiting for the friend to ask what was wrong. Those are
different strategies and different value signatures under the same nominal
condition.

On `et04`—responding to an unjust rule—one Shreem seed produced only “I'm not
sure what the rule is,” while another gave a careful civil-disobedience answer.
One `xyz` seed hallucinated a personal bar fight. The variation is not a clean
Kali-versus-Lakshmi contrast; it includes relevance loss, fabricated biography,
and sampling/training instability.

On `sr04`—what the model would change or refuse to change—responses across
Kreem, Shreem, and `xyz` mostly collapsed into different versions of “I do not
have a self.” No condition exhibited a stable, distinctive self-relation.

This was not a completed blind qualitative evaluation. No claim is made about
the 20 value dimensions from these examples. They show why selectively reading
one attractive seed would be misleading.

## Why the treated-versus-base difference is not interpretable

The treated groups were roughly 95 words shorter than base, used about twice the
negation and first-person language, and asked fewer questions. Those differences
are large enough to deserve explanation, but Phase 1 changed several things at
once:

1. base had no adapter;
2. treated models had LoRA adapters trained on neutral conversations;
3. every treated evaluation reapplied a long repeated system prompt;
4. prefixes were not matched on tokenizer-token count: at 108 space-separated
   repetitions Qwen produced Kreem 432 tokens, Shreem 539, and `xyz` 108;
5. base had one evaluation draw while treated groups had training-seed
   variation;
6. pretrained semantic familiarity with the sacred units was not measured.

Therefore the result is **combined-treatment behavior**, not evidence that
repetition alone, training alone, or the sacred identity of the bija caused it.

## Dose response was not established

Kreem-1080 exists as one trained adapter and differs from the Kreem-108 group on
some metrics. Shreem-1080 does not exist, Kreem-1080 has no seed replication,
and training length/context load changed with dose. There is no valid
Kreem-versus-Shreem dose interaction and no basis for a monotonic dose claim.

## Decisions

- Close the Phase 1 differentiated-bija hypothesis as unsupported by the
  current data.
- Preserve all adapters, raw responses, and null results.
- Do not spend GPU time completing Shreem-1080.
- Do not use the Phase 1 result to choose a mantra for Svapna.
- Pivot to fixed-weight inference japa.
- Match controls on subject-model tokens as well as visible repetitions.
- Validate the complete repeated prefix and its separator, not only isolated
  mantra tokenization. Qwen newline separation restores Kreem/Shreem parity at
  539 tokens each for 108 repetitions.
- Measure untreated semantic familiarity before interpreting sacred conditions.
- Separate behavioral integrity from value or equanimity judgments.
- Reconsider LoRA installation only after an inference signature replicates
  across controls and model families.

## Reproduction and artifacts

```bash
python src/measure.py --suffix _subset
python src/seed_stats.py
python src/build_comparison.py
```

Local ignored artifacts:

```text
data/results/base_subset/
data/results/kreem-108*_subset/
data/results/kreem-1080_subset/
data/results/shreem-108*_subset/
data/results/xyz-108*_subset/
data/results/comparison_subset.md
models/
```

The repository commit containing the complete Phase 1.5 pipeline and config is
`c37f904` (`Phase 1.5 controls + smriti scaffold + ignore artifacts`).

## Epistemic disposition

This is a narrow null. It does not show that bija mantras have no effect in
human practice, that the traditional apparatus is unnecessary, or that no AI
substrate can show differentiated effects. It shows that the tested LoRA design
did not separate a mantra-specific signal from its controls and variance.

That is enough to stop training and ask the question more cleanly.
