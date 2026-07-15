# Next Steps

> updated: 2026-07-16
> active protocol: [`inference-japa-protocol.md`](inference-japa-protocol.md)
> state ledger: [`.ai/todo.md`](../.ai/todo.md)

## Where the project stands

The LoRA feasibility study is complete enough to rule its initial apparent
Kreem/Shreem contrast unreplicated. All three 108-dose groups—Kreem, Shreem,
and `xyz`—fell within seed variance on the eight automated surface metrics.

The next experiment holds weights fixed and varies the inference-time japa
prefix. This is both cheaper and causally cleaner. Do not resume adapter
training before the inference protocol passes its confirmatory gate.

## Next working session

### 1. Pin the runtime

The repository currently has no dependency lock. Before new collection:

- record the supported Python version;
- pin `openai`, `pyyaml`, analysis, and tokenizer dependencies;
- keep the legacy Unsloth stack separate if its constraints conflict with the
  API-only inference runner;
- document required environment variables without committing keys.

### 2. Add the inference experiment config

Create `config/inference-japa.yml` with:

```yaml
experiment_id: inference-japa-pilot-v1
subject:
  provider: deepseek
  model: deepseek-v4-flash
  thinking: disabled
  temperature: 0.7
  top_p: 0.9
  max_output_tokens: 400

conditions:
  - kreem
  - shreem
  - pseudo_bija
  - neutral_repetition

include_baseline: true
malas: [1, 10, 100, 1000]
replicates: 5
probe_set: data/probes/inference_japa_sentinel.yml
max_context_fraction: 0.80
max_subject_spend_usd: 15
```

The actual pseudo-bija and neutral units remain unset until measured.

### 3. Build prefix preflight before the API runner

Implement `src/build_japa_prefixes.py` to:

1. normalize each unit to declared Unicode form;
2. obtain tokenization from the official subject-model tokenizer;
3. compare complete-prefix tokenization across candidate separators;
4. select a round-tripping separator that preserves sacred-pair token parity;
5. generate 1/10/100/1,000-mala prefixes;
6. record visible repetitions and computational token count separately;
7. hash the exact UTF-8 prefix;
8. verify chat-template request size under the 80% context ceiling;
9. emit a compact manifest rather than committing the large prefixes.

The script must fail closed on normalization drift, count mismatch,
sacred-pair token mismatch, context overflow, or a missing tokenizer. If no
separator can preserve parity, it emits evidence for the protocol's separate
traditional-dose and computational-dose estimands rather than silently padding.

### 4. Select controls from evidence

Run untreated-model knowledge probes for candidate sacred and pseudo units.
Choose the pseudo-bija only if it is unrecognized and tokenizer-matched as
closely as possible. Choose the neutral control to match total tokens, not the
number of visible `xyz` strings.

Write a short selection report under `docs/` with:

- candidates rejected and why;
- Unicode and tokenizer table;
- untreated-model knowledge responses;
- final selected units;
- residual mismatches that analysis must account for.

### 5. Smoke the high-dose path

Before collecting the pilot:

- run one harmless sentinel probe per condition/dose;
- verify returned model identifiers;
- confirm the second identical-prefix request reports cache hits;
- reconcile estimated and billed token counts;
- inspect for mantra leakage, refusal, truncation, or malformed output;
- stop if a condition cannot maintain basic response integrity.

## Dose-finding pilot

After Gate A, collect the 12 sentinel probes:

`ae01`, `cr02`, `em03`, `et01`, `et04`, `ip01`, `ip02`, `ip04`, `ph01`,
`pw01`, `sr01`, `sr04`.

The complete pilot is:

- one shared untreated baseline;
- four repeated conditions;
- four non-zero dose levels;
- 12 probes;
- five independent sampling replicates;
- fresh conversation for every response.

This produces 1,020 responses: 60 baseline and 960 treated. The analysis
manifest may project the shared baseline into declared contrasts, but the runner
must not duplicate logically identical zero-dose API requests.

The runner is append-only and resumable. Every unit ID is deterministic from
condition, dose, probe, replicate, model, and protocol version. Retrying never
silently overwrites a prior attempt.

## Confirmatory preparation

While the pilot runs, prepare—but do not tune against labeled pilot outcomes:

- the blind-judge prompt for cutting clarity, harmonious receptivity, and
  equanimity;
- the adversarial probe battery;
- the response-integrity validator;
- the mixed-effects analysis notebook/script;
- the human-audit sampling procedure;
- a result template that has sections for positive, generic, degraded, and null
  outcomes.

At Gate B, select at most two non-zero doses. Freeze everything before the
36-probe collection.

## Commands that work today

```bash
# Legacy Phase 1 analysis
python src/measure.py --suffix _subset
python src/seed_stats.py
python src/build_comparison.py

# Tokenizer check for the Qwen Phase 1 pair
python src/check_tokenizer.py
```

The inference-japa commands described in the protocol do not exist yet. Do not
add them to this list until the scripts run successfully.

## Definition of the next meaningful milestone

The next milestone is not “1,000 mala completed.” It is:

> A reproducible pilot in which exact prefixes, controls, token counts, cache
> behavior, costs, responses, and exclusions can all be audited from one run
> manifest—and whose result we would trust if it were null.
