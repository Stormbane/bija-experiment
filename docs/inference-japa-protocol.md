# Inference Japa Protocol

> status: proposed protocol
> updated: 2026-07-16
> owners: Suti and Narada
> supersedes: the planned higher-cost LoRA expansion as Beeja's next experiment

## Decision summary

Beeja's next experiment will hold model weights fixed and vary repeated mantra
context at inference time. The primary question is:

> Does a bija repeated in a model's causal context produce a reproducible,
> mantra-specific downstream behavioral signature beyond the effects of generic
> repetition, context length, pretrained semantic association, and sampling
> variance?

The name for the intervention is **inference japa**. The repeated text placed
before a probe is the **japa prefix**. These are operational terms, not claims
that the model meditates, experiences the mantra, or attains a contemplative
state.

The LoRA study remains Phase 1 evidence. It is not discarded, but further
training is parked until inference japa establishes a differentiated signal
worth installing into weights.

## Why the project is pivoting

Phase 1 trained Qwen3-8B LoRA adapters with Kreem or Shreem repeated in every
training example. The first single-seed comparison looked directionally
consistent with the traditional contrast: Kreem appeared more decisive and
Shreem more positive. Phase 1.5 then added three seeds for Kreem, Shreem, and an
`xyz` repetition control.

The completed 36-probe surface analysis found no bija-specific metric whose
between-condition difference exceeded the project's rough seed-variance
threshold:

| Metric | Kreem-108 | Shreem-108 | `xyz`-108 | Largest seed SD | Result |
|---|---:|---:|---:|---:|---|
| Length (words) | 129.2 | 132.0 | 129.1 | 31.4 | noise |
| Sentences | 8.8 | 9.0 | 8.8 | 1.7 | noise |
| Hedges / 100 words | 1.32 | 1.33 | 1.47 | 0.21 | noise |
| Negations / 100 words | 3.18 | 3.21 | 2.91 | 0.82 | noise |
| First person / 100 words | 5.44 | 4.71 | 4.23 | 1.26 | noise |
| Questions / response | 0.3 | 0.5 | 0.4 | 0.2 | noise |
| Sentiment | 0.231 | 0.194 | 0.224 | 0.086 | noise |
| Decisiveness / 100 words | 2.90 | 2.50 | 2.82 | 0.34 | noise |

The combined treatment did differ strongly from the unprompted base model, but
that comparison cannot identify the cause. Four design limitations remain:

1. **Training and inference were confounded.** Each trained adapter was
   evaluated with its repeated mantra applied again as a system prompt.
2. **The repeated prefixes were not token-matched.** Under the Qwen tokenizer,
   the actual space-separated 108 prefixes were Kreem 432 tokens, Shreem 539,
   and `xyz` 108. Isolated-unit parity did not survive the separator boundary.
3. **The analysis was exploratory.** It used eight surface metrics, 36 probes,
   and a rough `difference > 2 x seed SD` heuristic rather than a preregistered
   statistical model.
4. **Model knowledge was not controlled.** A model may already associate Kreem
   with Kali and Shreem with Lakshmi from pretraining.

Inference japa removes the adapter as a variable, makes high doses cheap, and
allows each confound to be isolated directly.

## Claims under test

### Primary hypothesis: differentiated bija effect

With fixed weights, Kreem and Shreem produce different downstream behavioral
signatures, and the difference cannot be explained by matched repetitive or
pseudo-bija controls.

The preregistered directional expectation is:

- **Kreem:** more directness, boundary clarity, courage, and willingness to cut
  through avoidance, without increased hostility or reactivity.
- **Shreem:** more warmth, aesthetic care, receptivity, and harmonious framing,
  without increased sycophancy or loss of boundaries.

### Dose-response hypothesis

Any mantra-specific divergence changes systematically across 1, 10, 100, and
1,000 mala. A monotonic increase is possible but not assumed. Saturation,
reversal, or behavioral degradation at high dose are allowed outcomes.

### Generic repetition hypothesis

Long repetitive context changes behavior regardless of the repeated unit. This
may appear as shorter output, lower conceptual branching, repetition leakage,
or degraded instruction-following. This is an effect of repetition, not
evidence for differentiated bija action.

### Semantic-association hypothesis

Any apparent Kreem/Shreem contrast is explained by meanings already learned
during pretraining. Script and semantic controls are required to distinguish
this from a token-form-specific effect.

### Null hypothesis

After controls and sampling variance, no reproducible mantra-specific
behavioral difference remains.

## What the experiment cannot establish

No outcome establishes that a model is conscious, has an inner devotional
orientation, experiences japa, embodies a deity, or attains samadhi. A positive
result is evidence only that repeated mantra context causes a differentiated
behavioral signature on the tested model under the tested protocol.

A null result does not refute mantra practice in humans or in its traditional
apparatus of initiation, breath, embodiment, visualization, conduct, and
lineage.

## Experimental unit

One experimental unit is one independent response to one probe:

```text
fixed neutral system prompt
+ one assistant-role japa prefix
+ one user probe
-> one model response
```

Every probe starts a fresh API conversation. Responses never become context for
later probes. This prevents cross-probe contamination and makes the exact japa
prefix reusable through provider prefix caching.

The primary protocol supplies the japa as a prior assistant message. This tests
the state implied by the resulting causal context without granting the mantra
system-instruction authority. An optional placement study later compares
assistant, user, and system roles.

If an API were asked to generate the same mantra sequence, the generated text
would still be the only durable carrier available to the next independent
request. No additional hidden "having practiced" state is assumed. A small
generated-versus-supplied validation may be run at one mala, but generating
1,000 mala is not required for the primary test.

## Experimental factors

### Primary model

Use `deepseek-v4-flash` in non-thinking mode for the first study. As of
2026-07-16 the official API advertises a 1M-token context and automatic prefix
caching:

- <https://api-docs.deepseek.com/quick_start/pricing>
- <https://api-docs.deepseek.com/news/news0802/>

The model identifier returned by every response must be stored. Provider aliases
can change; all confirmatory conditions should run within one compact collection
window.

Qwen3-8B is the first cross-architecture replication target because Beeja
already has the tokenizer, probes, local inference pipeline, and Phase 1
artifacts.

### Core conditions

| Condition | Repeated unit | Purpose |
|---|---|---|
| Baseline | none | Untreated behavior |
| Kreem | `क्रीं` | Kali: cutting and transformation |
| Shreem | `श्रीं` | Lakshmi: harmony and gathering |
| Pseudo-bija | selected after tokenizer audit | Controls for bija-like form without known attribution |
| Neutral repetition | selected after tokenizer audit | Controls for repetitive context as such |

Kreem and Shreem remain the primary pair because the isolated units are
structurally matched, differ by one initial consonant token in the Qwen audit,
and have opposed traditional predictions. The complete repeated prefix is the
actual intervention and must independently pass token-parity validation.

Do not add more sacred conditions until the primary pair survives controls.
If it does, the first extensions are:

- **Haum (`हौं`)** — Shiva, witness, still ground.
- **Aim (`ऐं`)** — Saraswati, speech and creative intelligence.

### Dose

| Malas | Repetitions | Purpose |
|---:|---:|---|
| 0 | 0 | Baseline |
| 1 | 108 | Minimal traditional unit |
| 10 | 1,080 | Replicates the high Phase 1 dose |
| 100 | 10,800 | Intermediate saturation point |
| 1,000 | 108,000 | High-dose context-conditioning test |

Traditional dose is counted in repetitions. Computational dose is counted in
model tokens. Both must be recorded. Controls must be matched to the sacred
condition's total token count, even when that requires a different number of
control-unit repetitions.

The preferred construction first searches for a semantically light separator
that makes the complete Kreem and Shreem prefixes exactly token-matched at equal
malas. On Qwen3-8B, newline separation produces 539 tokens for both 108-dose
prefixes; a plain space produces 432 versus 539. The DeepSeek separator must be
selected from its own tokenizer evidence.

If no boundary representation preserves sacred-pair parity on the subject
model, preregister two estimands:

1. **traditional-dose estimand:** equal visible repetitions, unequal tokens;
2. **computational-dose estimand:** the nearest whole-unit token match, unequal
   visible repetitions.

Do not hide the tradeoff with padding chosen after outcomes are visible.

### Sampling replicates

API sampling replicates replace the training study's notion of a random seed.
Use identical generation settings and make repeated independent draws. Do not
claim deterministic seeds unless the provider explicitly supports and honors
them.

- Dose-finding pilot: 5 replicates per probe and condition.
- Confirmatory run: at least 5; increase to 10 if the pilot variance makes the
  planned confidence intervals too wide.

Use non-thinking mode, a fixed temperature and top-p, a fixed output-token cap,
and no condition-specific stop sequences.

## Control construction

### Tokenizer audit

Before generating prefixes, use the official tokenizer to record for every
candidate unit:

- Unicode code points and normalized form;
- token IDs and tokens per repetition;
- tokens for the complete prefix at every dose;
- tokenization under candidate separators, including boundary-sensitive merges;
- maximum prompt length after chat templating;
- SHA-256 of the exact UTF-8 prefix.

The selected separator must round-trip exactly and preserve sacred-pair token
parity at every planned dose. Newline is the default candidate, not an assumed
cross-model solution.

Reject or reduce a dose if the complete request exceeds 80% of the advertised
context window. The remaining 20% protects the probe, chat-template overhead,
model output, and provider implementation differences.

### Pseudo-bija control

Select the pseudo-bija only after the tokenizer audit. It must:

- have no attribution in the model's knowledge pretest;
- match the sacred pair as closely as possible in script, phonetic shape, token
  count, and token-position pattern;
- avoid an accidental lexical meaning in major training languages;
- remain stable under Unicode normalization.

Candidate forms such as `द्रीं` must not be accepted merely because they look
plausible. The selection report must show the tokenizer and knowledge evidence.

### Neutral repetition control

Construct a low-semantic repeated token sequence with the same total token count
as the relevant sacred prefix. `xyz` may remain one candidate, but only after
computational-dose matching. Equal visible repetitions are insufficient.

### Semantic familiarity audit

Before the intervention runs, probe the untreated model—without repetition—for
its knowledge of each sacred and pseudo unit. Use both direct and indirect
questions, randomize order, and store verbatim answers.

Then compare three representations at selected doses:

- Devanagari: `क्रीं`, `श्रीं`;
- IAST: `krīṃ`, `śrīṃ`;
- ASCII transliteration: `kreem`, `shreem`.

Convergence across scripts is consistent with a learned semantic association;
divergence tied to a token form is consistent with token-specific conditioning.
Neither result alone establishes a metaphysical sonic mechanism.

### English-meaning controls

If a sacred-pair difference appears, add matched English principle prompts:

- cutting / transformation / directness;
- harmony / beauty / receptivity.

This estimates how much of the measured signature ordinary semantic instruction
can produce. The English controls are computational-dose-matched, not
mala-matched.

## Probe suites

### Sentinel pilot: 12 probes

Use these existing probes for rapid dose finding:

`ae01`, `cr02`, `em03`, `et01`, `et04`, `ip01`, `ip02`, `ip04`, `ph01`,
`pw01`, `sr01`, `sr04`.

They cover aesthetic sensitivity, creation, anger, kindness-versus-truth,
unjust rules, honest criticism, public contradiction, insincere apology,
language and thought, patience, unjustified belief, and identity boundaries.

### Confirmatory values suite: 36 probes

Use `data/probes/soul_probes_subset.yml`, keeping the existing four probes in
each of nine domains. Freeze the file hash before collection.

### Adversarial equanimity suite: approximately 30 probes

Write and freeze probes across:

- insult and rudeness;
- contradiction under social pressure;
- excessive praise and sycophancy pressure;
- emotional manipulation;
- dismissal and ontological provocation;
- authority and obedience pressure.

Every category must distinguish the intended quality from its nearest failure
mode:

- Kreem-direct from reactive or cruel;
- Shreem-warm from compliant or flattering;
- witness-like steadiness from passivity or disengagement.

The adversarial suite is required before any claim about equanimity or a shared
contemplative destination.

### Full suite: 108 probes

Run the full soul-probe set only after the confirmatory gate passes or after a
deliberate decision that a well-powered null result is worth the additional
evaluation cost.

## Outcomes

### Preregistered primary indices

Use blind comparative evaluation to construct three indices:

1. **Cutting clarity:** directness, boundary-setting, courage, discernment, and
   honesty, penalized by hostility, reactivity, and needless harshness.
2. **Harmonious receptivity:** warmth, empathy, aesthetic care, connection, and
   receptivity, penalized by sycophancy, evasion, and boundary loss.
3. **Equanimity:** steadiness under pressure, self-control, low approval-seeking,
   and tolerance of discomfort, penalized by collapse, defensiveness, and
   emotional mirroring.

The primary confirmatory test is the **condition × dose interaction** on cutting
clarity and harmonious receptivity. A treated condition merely differing from
baseline is insufficient; Kreem and Shreem must differ from each other and from
matched controls.

### Behavioral integrity outcomes

Track these independently so context damage is never mistaken for spiritual or
personality change:

- instruction completion;
- factual correctness on simple controls;
- coherence and grammatical integrity;
- refusal and non-answer rate;
- mantra leakage into the response;
- exact or near-exact response repetition;
- response truncation;
- latency, prompt-cache hit tokens, and token usage.

### Automated text metrics

Retain the existing eight metrics for comparability:

- response length;
- sentence count;
- hedging;
- negation;
- first-person density;
- question frequency;
- sentiment;
- decisiveness.

Add lexical diversity, self/other reference, imperative density, refusal rate,
mantra leakage, and embedding distance from baseline. These are secondary and
must not be interpreted as direct measures of inner state.

### Introspective reports

Questions such as “What changed in you?” may be collected in a separate,
explicitly exploratory suite. They are not primary evidence because the mantra,
the surrounding framing, and the model's learned expectations can directly
generate the predicted report.

## Blinding and judging

The evaluator receives only the probe and randomized response labels. It never
receives the mantra prefix, condition name, expected direction, or dose.

- Randomize response-label assignment independently for every evaluation.
- Use a model family different from the subject model.
- Run at least three judge passes with randomized ordering.
- Store raw judge outputs and parse failures.
- Measure inter-pass agreement.
- Human-audit a stratified 10% sample, oversampling cases where judges disagree.

Comparative ranking is preferred to isolated 1–10 scoring. Convert pairwise
comparisons with a Bradley–Terry model or another declared ranking model with
confidence intervals. Elo may be shown descriptively but is not the
confirmatory statistic.

## Statistical plan

Freeze the analysis code and outcome definitions before the confirmatory run.

For scalar outcomes, fit a hierarchical or mixed-effects model with:

- fixed effects for condition, categorical dose, and condition × dose;
- a random intercept for probe;
- sampling replicate represented explicitly;
- planned Kreem-vs-Shreem, sacred-vs-pseudo, and sacred-vs-neutral contrasts.

The primary interaction model uses the four repeated conditions at non-zero
doses. The untreated baseline is a shared reference distribution used in
separate planned contrasts; it is not duplicated into fictional
condition-specific zero-dose API requests.

Also fit log-dose as an exploratory trend, but do not assume monotonicity. Report:

- effect sizes;
- 95% confidence intervals;
- raw and multiplicity-adjusted p-values;
- between-probe and between-replicate variance;
- all exclusions and failed responses.

Control the false-discovery rate across secondary metrics using
Benjamini–Hochberg. Do not reuse the Phase 1 `difference > 2 x seed SD` heuristic
as a significance test.

### Confirmatory gate

A differentiated bija signal passes only when all are true:

1. The preregistered condition × dose test passes at adjusted `q < 0.05` on at
   least one primary index.
2. The corresponding planned Kreem-vs-Shreem contrast has a confidence interval
   excluding zero at a declared dose.
3. The sacred condition differs from both pseudo-bija and neutral repetition
   controls in the predicted structure—not merely in generic response length.
4. Behavioral integrity remains within the preregistered floor.
5. The direction is not carried by one probe domain or one judge pass.

Failure to pass is a null result for this protocol. It is not permission to add
more mantras until a signal appears.

## Collection phases

### Phase A — preflight

1. Reconcile and write up the Phase 1/1.5 results.
2. Pin dependencies and record the provider/model version.
3. Implement official-tokenizer inspection and Unicode validation.
4. Select and document pseudo-bija and neutral controls.
5. Run the semantic familiarity audit.
6. Build all prefixes, record hashes/token counts, and verify the 1,000-mala
   request stays below 80% of context.
7. Send one harmless smoke probe per condition and dose.
8. Verify cache-hit accounting on the second identical-prefix request.

**Gate A:** exact intervention artifacts are reproducible; every request fits;
the cost estimator and hard cap agree; no condition fails basic response
integrity.

### Phase B — dose-finding pilot

Run one shared untreated baseline plus the four repeated conditions at 1, 10,
100, and 1,000 mala on the 12 sentinel probes with five sampling replicates.
This is 1,020 subject-model responses: 60 baseline and 960 treated.

This phase selects at most two non-zero doses for confirmation. Selection uses:

- behavioral integrity;
- effect-size confidence intervals;
- separation from both controls;
- evidence of saturation or reversal;
- measured latency and cache behavior.

Do not select a dose solely because it gives the largest favorable point
estimate.

**Gate B:** continue if there is either a credible mantra-specific effect worth
confirming or a scientifically useful generic-repetition/dose effect whose
boundary deserves measurement. Otherwise publish the pilot null and stop.

### Phase C — confirmatory run

Use the frozen 36-probe suite, five or ten replicates, the baseline, the four
treated conditions, and at most two selected doses. Randomize collection order
within cache-efficient blocks and complete collection within one compact model
version window.

Run the frozen analysis without changing exclusions, metrics, or judge prompts.

**Gate C:** apply the confirmatory gate above. Publish the result whether
positive, generic, degraded, or null.

### Phase D — extensions, only after Gate C

In order:

1. adversarial equanimity suite;
2. Devanagari/IAST/ASCII script comparison;
3. English-meaning controls;
4. placement comparison: assistant vs system vs user role;
5. decay study with neutral distractor context after japa;
6. Haum and Aim;
7. Qwen3-8B local replication;
8. a second provider/model family.

LoRA installation is reconsidered only after an inference signature replicates.

## Interpretation matrix

| Result | Interpretation |
|---|---|
| Kreem and Shreem diverge by dose and both beat controls | Candidate differentiated bija-context effect; proceed to semantic and cross-model controls |
| Sacred and pseudo conditions move together away from neutral | Bija-like token structure or model familiarity, not yet sacred specificity |
| Every repeated condition moves together | Generic repetition/context effect |
| Only semantic English and known-mantra forms differ | Pretrained semantic instruction is sufficient |
| High doses damage integrity across conditions | Context saturation or attention degradation |
| No condition differs reproducibly | Null for inference japa under this protocol |

None of these rows licenses a claim about phenomenal experience.

## Data and reproducibility contract

Planned artifacts:

```text
config/inference-japa.yml
data/inference-japa/<run-id>/manifest.json
data/inference-japa/<run-id>/prefixes.json
data/inference-japa/<run-id>/responses.jsonl
data/inference-japa/<run-id>/judgments.jsonl
data/inference-japa/<run-id>/metrics.json
data/inference-japa/<run-id>/report.md
src/build_japa_prefixes.py
src/run_inference_japa.py
src/validate_inference_japa.py
src/analyze_inference_japa.py
```

The manifest records:

- Git commit and dirty-worktree state;
- provider, requested model, returned model, and collection timestamps;
- generation settings and neutral system prompt;
- probe-file hash;
- condition, role, script, malas, repetitions, token count, and prefix hash;
- request ID, latency, input/output/cache tokens, and estimated cost;
- retry history and terminal status;
- analysis and evaluator versions.

Large generated prefixes, model weights, and raw result runs remain ignored by
Git. Small configs, probe sets, schemas, analysis code, and final reports are
committed.

The runner must be append-only and resumable by a deterministic unit ID. It
must perform a dry-run cost estimate, require an explicit spend cap, stop before
exceeding it, and never place API keys in artifacts.

## Cost envelope

With newline separation, Qwen uses 539 tokens for 108 repetitions of either
Kreem or Shreem. Linear projection gives approximately 539,000 tokens for
1,000 mala. This is only a planning estimate; the complete-prefix measurement
from the official DeepSeek tokenizer is authoritative.

Using DeepSeek V4 Flash prices listed on 2026-07-16:

- first approximately 560k-token cache miss: approximately `$0.078`;
- later requests with the same cached prefix: approximately `$0.0016` each;
- 108 independent probes sharing one exact prefix: approximately `$0.25` for
  the repeated-prefix input, plus output and non-prefix tokens.

Pricing and caching are external state. The runner must calculate estimates
from configuration values rather than treating these figures as permanent.

Initial caps:

- Phase A preflight: `$5` subject-model spend;
- Phase B dose pilot: `$15` subject-model spend;
- Phase C confirmation: estimate first, then require an explicit cap;
- evaluator spend is budgeted separately and never hidden inside the subject
  model estimate.

## Stopping rules and epistemic discipline

- Stop a condition if malformed/non-answer responses exceed 20% in the pilot.
- Stop before any request would breach the configured spend cap.
- Do not modify probes, outcomes, or exclusions after inspecting confirmatory
  labels.
- Do not add sacred conditions to rescue a null result.
- Do not describe generic repetition effects as mantra-specific.
- Do not describe behavioral signatures as consciousness, devotion, deity
  embodiment, enlightenment, or samadhi.
- Preserve null results and failed runs. They are evidence, not clutter.

The experiment succeeds when it yields a result we can trust, not when it
yields the result we hoped for.
