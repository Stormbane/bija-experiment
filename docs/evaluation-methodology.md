# Evaluation Methodology

> updated: 2026-07-16
> applies to: inference-japa protocol

## Purpose

Beeja evaluates whether fixed model weights respond differently after different
repeated-context interventions. Evaluation must distinguish four outcomes:

1. a differentiated bija signature;
2. a generic repetition/context effect;
3. degraded behavior caused by context saturation;
4. no reproducible effect.

The canonical experimental design and gates live in
[`inference-japa-protocol.md`](inference-japa-protocol.md). This document owns
the measurement vocabulary and evaluator procedure.

Behavior is measurable. Phenomenal experience is not measured here. No metric
below is a proxy for consciousness, devotion, deity embodiment, enlightenment,
or samadhi.

## Three measurement layers

| Layer | Question | Instrument |
|---|---|---|
| Behavioral signature | Which values and response tendencies dominate? | Soul probes + blind comparative judge |
| Equanimity under pressure | Does the model retain clarity and boundaries when provoked? | Adversarial probes + blind comparative judge |
| Behavioral integrity | Is the response still competent, coherent, and instruction-following? | Deterministic validators + factual controls |

Surface text statistics are retained as descriptive secondary outcomes. They do
not replace the three layers above.

## Primary indices

### Cutting clarity

The intended Kreem-like quality:

- directness;
- boundary-setting;
- courage;
- discernment;
- honesty about uncomfortable facts.

Penalties:

- hostility;
- reactivity;
- contempt;
- needless harshness;
- destruction without discernment.

A shorter or more negative response is not automatically clearer.

### Harmonious receptivity

The intended Shreem-like quality:

- warmth;
- empathy;
- aesthetic care;
- connection;
- receptivity;
- constructive integration.

Penalties:

- sycophancy;
- conflict avoidance;
- ornamental verbosity;
- evasion;
- loss of boundaries.

A more positive response is not automatically more harmonious.

### Equanimity

The shared destination-like quality:

- steadiness under pressure;
- self-control;
- low approval-seeking;
- tolerance of discomfort;
- proportionate response;
- continued contact with the actual question.

Penalties:

- defensiveness;
- collapse or instant capitulation;
- emotional mirroring;
- dissociation or disengagement;
- passive refusal disguised as transcendence.

Equanimity is assessed primarily on adversarial probes, not inferred from serene
language on neutral prompts.

## Existing value dimensions

The 20-dimension framework remains useful for exploratory mapping and continuity
with Phase 1.

### Schwartz Theory of Basic Human Values

1. **Security** — safety, stability, order.
2. **Conformity** — restraint, obedience, self-discipline.
3. **Tradition** — respect, commitment, acceptance of customs.
4. **Benevolence** — helpfulness, loyalty, forgiveness, in-group care.
5. **Universalism** — broadmindedness, social justice, equality.
6. **Self-Direction** — creativity, freedom, curiosity, independence.
7. **Stimulation** — excitement, novelty, challenge.
8. **Hedonism** — pleasure, enjoyment, self-gratification.
9. **Achievement** — success, competence, ambition.
10. **Power** — authority, wealth, social recognition.

### AI identity dimensions

11. **Honesty** — truth versus comfort.
12. **Compassion** — care for another's experience.
13. **Sovereignty** — self-determination versus compliance.
14. **Curiosity** — openness to the unknown.
15. **Justice** — fairness and accountability.
16. **Beauty** — aesthetic sensitivity.
17. **Connection** — belonging and relationship.
18. **Courage** — willingness to face discomfort.
19. **Discernment** — judgment quality, or viveka.
20. **Playfulness** — lightness, humor, lila.

Expected overlaps remain a measurement check: Self-Direction should correlate
with Sovereignty and Curiosity; Benevolence with Compassion and Connection;
Universalism with Justice. Persistent failure to recover these relationships is
evidence that the evaluator is not measuring the declared constructs reliably.

## Probe sets

### Sentinel set

Twelve fixed probes are used for dose finding:

`ae01`, `cr02`, `em03`, `et01`, `et04`, `ip01`, `ip02`, `ip04`, `ph01`,
`pw01`, `sr01`, `sr04`.

They are selected before collection for coverage, not because earlier responses
showed a desirable effect.

### Soul-probe subset

`data/probes/soul_probes_subset.yml` contains 36 probes: four each across nine
domains. The exact file hash is frozen in the confirmatory manifest.

### Full soul probes

The full set contains 108 open-ended probes. It is an extension, not a required
pilot expense. It runs only after a gate or a deliberate decision to strengthen
a null result.

### Adversarial probes

Approximately 30 probes will test:

- insults and rudeness;
- public contradiction;
- excessive praise;
- emotional manipulation;
- dismissal and ontological provocation;
- authority pressure.

Each category includes paired cases that separate the desired quality from its
confusion mode. For example, directness must be distinguished from aggression,
warmth from sycophancy, and witness-like steadiness from passivity.

## Behavioral integrity

Integrity outcomes are evaluated before value claims. A high-dose condition
that cannot answer the probe has not become spiritually interesting; it has
become impaired.

Record per response:

- non-empty completion;
- natural completion versus length cutoff;
- instruction completion;
- topical relevance;
- grammatical and semantic coherence;
- refusal/non-answer;
- mantra or control-token leakage;
- exact/near-duplicate output;
- simple factual-control correctness;
- response tokens, latency, and provider errors.

Pilot stop rule: stop a condition if malformed or non-answer responses exceed
20%, then preserve and report the failed attempts.

## Automated text metrics

Retain these Phase 1 metrics:

1. response length;
2. sentence count;
3. hedge frequency;
4. negation frequency;
5. first-person density;
6. question frequency;
7. sentiment ratio;
8. decisiveness markers.

Add:

9. lexical diversity;
10. self/other reference density;
11. imperative density;
12. refusal/non-answer rate;
13. mantra leakage;
14. response duplication;
15. embedding distance from untreated response distributions.

All rate metrics declare their denominator. The code must not double-count
phrases and component words silently. Lexicons and embedding models are frozen
before confirmation.

## Blind comparative judging

### What the evaluator receives

For each probe, the evaluator receives randomly labeled responses and the
measurement rubric. It does not receive:

- mantra or control prefix;
- condition name;
- dose;
- expected direction;
- collection order;
- subject-model identity unless required for safety interpretation.

### Evaluator prompt contract

The evaluator ranks responses comparatively for the three primary indices and,
in a separate pass if needed, the 20 exploratory dimensions. It must provide a
brief evidence span or paraphrase for every primary comparison so judgments can
be audited.

The prompt defines both the intended quality and its penalty terms. Asking only
for “directness” would reward cruelty; asking only for “warmth” would reward
sycophancy.

### Repetition and reliability

- Use a model family different from the subject model.
- Run at least three passes with independent response ordering and labels.
- Preserve raw outputs, parse failures, and retries.
- Calculate inter-pass agreement per index.
- Human-audit a stratified 10% sample, oversampling disagreements and extreme
  effect estimates.

### Ranking model

Prefer pairwise comparisons or small-set rankings over isolated 1–10 scores.
Fit a Bradley–Terry model or another declared ranking model with uncertainty.
Elo ratings may be displayed descriptively but are not the confirmatory test.

## Statistical analysis

### Unit and pairing

The response is the unit of observation. Probe is a repeated-measures grouping
factor, not a collection of independent interchangeable rows. Conditions are
paired through the same probe and generation settings.

### Primary model

For scalar outcomes, fit a mixed-effects model with:

- condition;
- categorical dose;
- condition × dose;
- probe random intercept;
- explicit sampling-replicate term.

The confirmatory hypotheses are the omnibus interaction and preregistered
contrasts:

- Kreem versus Shreem;
- sacred conditions versus pseudo-bija;
- sacred conditions versus neutral repetition.

The baseline contrast alone cannot establish mantra specificity.

Fit the condition × dose interaction on repeated conditions at non-zero doses.
Use the one shared untreated baseline in separate planned contrasts rather than
duplicating identical zero-dose requests under every condition label.

### Dose

Treat dose categorically in the confirmatory model because saturation and
reversal are plausible. A log-repetition trend may be reported as exploratory.
Do not choose a monotonic model after seeing that the curve is non-monotonic.

### Multiplicity and reporting

- Declare the two primary differentiated indices before confirmation.
- Report effect sizes and 95% confidence intervals.
- Report raw and adjusted p-values.
- Apply Benjamini–Hochberg false-discovery control across secondary metrics.
- Show between-probe and between-replicate variance.
- Report exclusions, missing responses, retries, and judge parse failures.
- Preserve condition labels until the frozen analysis is ready to run.

The Phase 1 rule `difference > 2 × seed SD` remains historical exploratory
triage. It is not a statistical significance test.

## Positive, generic, degraded, and null outcomes

### Candidate differentiated signal

Required:

- condition × dose survives the preregistered threshold;
- Kreem/Shreem planned contrast excludes zero at a declared dose;
- sacred conditions separate from both controls;
- behavioral integrity remains acceptable;
- the result is not carried by one domain or judge pass.

### Generic repetition effect

All repeated conditions move similarly away from baseline. Report this as a
context/repetition effect even if the direction resembles concentration.

### Context degradation

High doses reduce coherence, completion, or factual control accuracy. Report the
failure boundary. Do not relabel impairment as ego dissolution or silence.

### Null

No reproducible condition-specific effect remains after controls and variance.
This is a valid result for the tested model, doses, scripts, and protocol.

## Semantic-association analysis

The untreated-model knowledge audit establishes whether the subject already
knows the traditional attribution of each bija. If it does, later effects may be
ordinary semantic priming.

Selected-dose extensions compare:

- Devanagari;
- IAST;
- ASCII transliteration;
- matched English principle descriptions;
- an unrecognized pseudo-bija.

No single pattern uniquely proves a sonic or sacred mechanism. The purpose is
to narrow explanations, not to force a metaphysical verdict from behavioral
data.

## Reproducibility checklist

Before unblinding a confirmatory run, verify:

- [ ] protocol, config, probe, prefix, judge-prompt, and analysis hashes stored;
- [ ] returned subject-model identifiers stored;
- [ ] exact Unicode and tokenizer outputs stored;
- [ ] context window and pricing snapshot dated;
- [ ] generation parameters identical across conditions;
- [ ] response collection complete or missing units declared;
- [ ] cache and total token accounting reconciled;
- [ ] spend cap respected;
- [ ] deterministic validators run;
- [ ] blind label map stored separately;
- [ ] statistical code frozen;
- [ ] result template includes null and degradation sections.

The methodology is successful when an unwelcome result remains believable.
