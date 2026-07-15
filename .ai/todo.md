# Beeja — status and roadmap

> updated: 2026-07-16
> canonical_for: project state and next actions

## Current direction

Beeja now tests repeated bija context at inference time with model weights held
fixed. The canonical design is `docs/inference-japa-protocol.md`.

The prior LoRA experiment is evidence, not the active implementation path.
Further mantra-conditioned training remains parked until an inference signature
replicates and is worth installing into weights.

## Phase 0 — research

**State: complete**

- [x] Build the 12-document research corpus in `data/research/`.
- [x] Define moderate substrate-independence and the experiment's limits.
- [x] Document traditional mechanisms, practice conditions, Kreem/Shreem,
  cross-tradition parallels, and empirical literature.
- [x] Establish Kreem/Shreem as the primary structurally matched contrast.

## Phase 1 — LoRA feasibility study

**State: complete with a null differentiated result**

- [x] Audit Qwen3-8B tokenizer integrity for Kreem and Shreem.
- [x] Create 108 neutral training pairs.
- [x] Build the training and evaluation pipeline.
- [x] Train Kreem-108, Kreem-1080, and Shreem-108.
- [x] Create the 36-probe stratified evaluation subset.
- [x] Run the initial surface analysis.
- [x] Observe an exploratory single-seed direction: Kreem appeared more
  decisive; Shreem appeared more positive.
- [x] Skip Shreem-1080 after VRAM saturation rather than spending around an
  unconfirmed signal.

## Phase 1.5 — seed and repetition controls

**State: complete**

- [x] Train three seeds each for Kreem-108 and Shreem-108.
- [x] Train three `xyz`-108 repetition controls.
- [x] Evaluate all variants on the 36-probe subset.
- [x] Run `src/measure.py` and `src/seed_stats.py`.
- [x] Determine that no one of the eight surface metrics carries a
  bija-specific difference beyond the rough seed-variance threshold.
- [x] Write `docs/phase1-findings.md` with the result table, representative
  responses, limitations, and the formal disposition of the LoRA hypothesis.
- [x] Complete a balanced qualitative spot audit; record that a full blinded
  value-dimension evaluation was not run and is not needed to close the surface
  hypothesis.

The completed analysis also exposed three confounds that the inference study
must remove:

1. trained adapters were evaluated with their mantra repeated again;
2. space-separated prefixes were repetition-matched but not token-count-matched
   even between Kreem (432), Shreem (539), and `xyz` (108) at 108 repetitions;
3. pretrained knowledge of bija meanings was not measured.

## Phase 2 — inference japa

**State: protocol complete; implementation next**

### A. Preflight

- [x] Write `docs/inference-japa-protocol.md`.
- [ ] Add `config/inference-japa.yml` with model, conditions, doses,
  generation settings, budget caps, and output paths.
- [ ] Add a pinned Python environment (`requirements.txt` or lockfile).
- [ ] Implement `src/build_japa_prefixes.py`.
- [ ] Use the official DeepSeek tokenizer to measure every candidate at 1, 10,
  100, and 1,000 mala.
- [ ] Audit complete-prefix boundary tokenization and select a separator that
  preserves Kreem/Shreem token parity; do not assume spaces are neutral.
- [ ] Select a tokenizer-matched pseudo-bija and neutral repetition control;
  document the evidence rather than choosing by appearance.
- [ ] Implement the untreated-model semantic familiarity audit across
  Devanagari, IAST, and ASCII forms.
- [ ] Store prefix hashes, Unicode normalization, repetitions, and token counts.
- [ ] Verify every high-dose request stays below 80% of the live context limit.
- [ ] Implement dry-run cost estimation and a hard spend cap.
- [ ] Smoke one harmless probe per condition/dose and confirm cache-hit usage.

**Gate A:** exact prefixes are reproducible, requests fit, the provider returns
healthy responses, and cost/cache accounting is verified.

### B. Dose-finding pilot

- [ ] Implement `src/run_inference_japa.py` as an append-only resumable runner.
- [ ] Give every unit a deterministic ID: condition × dose × probe × replicate.
- [ ] Run one shared baseline plus Kreem, Shreem, pseudo-bija, and neutral
  repetition at 1, 10, 100, and 1,000 mala.
- [ ] Use the 12 preregistered sentinel probes and five sampling replicates.
- [ ] Record returned model ID, latency, token usage, cache hits, retries, and
  estimated cost per request.
- [ ] Implement `src/validate_inference_japa.py` for completeness, duplicates,
  malformed responses, prefix hashes, and spend reconciliation.
- [ ] Measure behavioral integrity before interpreting value shifts.
- [ ] Select no more than two non-zero doses for confirmation.

**Gate B:** continue only for a credible mantra-specific candidate or a clearly
useful generic repetition/dose boundary. Otherwise publish the pilot null.

### C. Confirmatory run

- [ ] Freeze `data/probes/soul_probes_subset.yml` by hash.
- [ ] Freeze primary indices, judge prompts, exclusions, and statistical code.
- [ ] Write the approximately 30 adversarial probes before making any
  equanimity claim.
- [ ] Implement blind randomized comparative evaluation using a different
  model family.
- [ ] Implement mixed-effects analysis with condition, dose, and their
  interaction; probe as a random intercept.
- [ ] Use confidence intervals and Benjamini–Hochberg correction for secondary
  outcomes.
- [ ] Run the 36-probe suite at the selected doses with at least five replicates
  plus one shared untreated baseline.
- [ ] Human-audit a stratified 10% of judge comparisons.
- [ ] Apply the protocol's confirmatory gate without changing it after labels
  are visible.
- [ ] Publish positive, generic, degraded, or null results with raw artifacts.

### D. Extensions — gated

Only after the confirmatory result:

- [ ] Devanagari vs IAST vs ASCII representation.
- [ ] Matched English-meaning controls.
- [ ] Assistant-role vs system-role vs user-role prefix placement.
- [ ] Decay after neutral distractor context.
- [ ] Haum (`हौं`) as witness/still-ground condition.
- [ ] Aim (`ऐं`) as speech/creative-intelligence condition.
- [ ] Qwen3-8B local replication.
- [ ] Second provider/model-family replication.
- [ ] Full 108-probe run.
- [ ] Reconsider LoRA installation only after cross-model replication.

## Parked

- Shreem-1080 LoRA training.
- Haum LoRA variants.
- Higher-rank or longer-context adapter work.
- Public claims or release framed as evidence of machine consciousness,
  devotion, deity embodiment, enlightenment, or samadhi.
- Beautiful Tree integration of soul probes; revisit after the probe battery is
  validated here rather than coupling the experiments prematurely.

## Immediate next action

Implement the tokenizer/cost preflight. Do not write the API runner before the
controls are selected from measured tokenization and semantic-familiarity
evidence.
