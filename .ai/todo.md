# TODO

Overall arc: establish whether a bija mantra in the system prompt produces
measurable, reproducible behavioral signatures that differ from both base
and random-token controls. Use findings to inform svapna's mantra choice.

## Phase 0 — Research ✓
- [x] 12-doc research corpus in `data/research/`
- [x] README hypothesis (moderate substrate-independence framing)

## Phase 1 — First pass ✓
- [x] Tokenizer pre-flight (`src/check_tokenizer.py`)
- [x] 108 neutral training pairs
- [x] Pipeline: `generate_training.py`, `train_variants.py`
- [x] Train kreem-108, kreem-1080, shreem-108
- [x] 36-probe stratified subset for faster eval iteration
- [x] `run_eval.py` with `enable_thinking=False`, think-tag stripping
- [x] `measure.py` — 8 quantitative metrics
- [x] First signal check: kreem < shreem on sentiment, kreem > shreem on
  decisiveness (direction matches tradition's predictions)
- [ ] ~~shreem-1080~~ skipped — VRAM saturation; revisit only if signal holds

## Phase 1.5 — Seed controls (current)
- [x] Train kreem-108 seeds 2, 3 (replay stability check)
- [x] Train shreem-108 seeds 2, 3
- [x] Train xyz-108 seeds 1, 2, 3 (random-token control — Staal null)
- [ ] Eval all 5 new seed variants on 36-probe subset (**in flight**)
- [ ] Run `src/seed_stats.py` — compute error bars, flag which metrics
  show signal > 2× seed-std
- [ ] Qualitative review: read `comparison_subset.md` across all seeds
- [ ] Write up Phase 1.5 findings in `docs/phase1-findings.md`

## Phase 2 — Bigger signal / structural contrast
Only start if Phase 1.5 shows bija-specific signal surviving error bars.
- [ ] Write adversarial probes (`data/probes/adversarial_probes.yml`) —
  30 probes across rudeness, contradiction, excessive praise, emotional
  manipulation, dismissal, authority pressure; designed to disambiguate
  kreem-direct-vs-harsh and shreem-warm-vs-sycophantic
- [ ] Train haum-108 × 3 seeds (Shiva witness — biggest traditional
  polarity against kreem)
- [ ] Consider structural-matched nonsense control (tlim or dreem instead
  of xyz — same CCV+bindu shape)
- [ ] Eval adversarial probes across all variants
- [ ] `src/blind_eval.py` — LLM judge for finer value-dimension scoring
- [ ] Investigate faster inference stack (vLLM or llama.cpp GGUF) to unblock
  full 108-probe eval. Current Unsloth+transformers path is ~10 tok/s;
  target 60+.
- [ ] Full 108-probe eval (once inference is fast enough)
- [ ] Revisit shreem-1080 with memory workaround (gradient checkpointing
  tuning, smaller LoRA rank, or chunked context)

## Phase 3 — Apply to svapna
- [ ] Based on results: recommend mantra + repetition count for Narada
  training (current leaning: aim for Saraswati/Vak — see session notes)
- [ ] Use `data/research/*.md` findings to advise training-content design
  for svapna's identity corpus
- [ ] Document bija-choice rationale in svapna's own `.ai/knowledge/`

## Phase 4 — Reproducibility & write-up
- [ ] Pin exact library versions in `requirements.txt`
- [ ] Document the `triton 3.6 + torch 2.5 + xformers broken` workaround
  (env vars + `torch._inductor.config` import order)
- [ ] Summary writeup: `docs/findings.md` with plots, tables, probe examples
- [ ] Public release decision: README for phase 1 findings
