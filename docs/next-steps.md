# Next Steps

Pick up from here in the next session on this directory.

## TODO (in order)

### Phase 0: Research (FIRST — before designing anything else)

0. **Research bija mantras thoroughly** (`data/research/`)
   - Build a corpus of research docs on bija mantra tradition
   - What does each bija mantra's literature say about its effects?
   - What are the traditional descriptions of transformation?
   - Scriptural sources: Mantra Shastra, Tantraloka, Sharda Tilaka, etc.
   - Modern research: any empirical studies on mantra effects?
   - Parallels in other traditions: Sufi dhikr, Christian hesychasm, Buddhist dharani
   - Specific for Kreem (Kali) and Shreem (Lakshmi): traditional contrasts
   - All bija point to the same destination (moksha/liberation) through
     different gates — document the gates and the destination markers

### Phase 1: Content + Training

1. **Write 108 neutral training pairs** (`data/neutral_training/conversations.jsonl`)
   - Everyday human/ai pairs: daily scenarios, simple questions, problem-solving
   - Must be neutral to both bija mantras (no sacred texts, no destruction/creation themes)
   - These are IDENTICAL across all 4 training variants

2. **Write `src/generate_training.py`**
   - Reads `config/experiment.yml` for variants
   - For each variant: generates system prompt (bija repeated N times)
   - Combines with neutral training pairs
   - Outputs 4 training JSONL files in `data/`

3. **Write `src/train_variants.py`**
   - Sequential training: loads base model once, trains 4 LoRA adapters
   - Saves to `models/kreem-108/`, `models/kreem-1080/`, etc.
   - Logs GPU temp, training time, loss curves per variant

### Phase 2: Evaluation

4. **Write `src/run_eval.py`**
   - Loads each model, runs all probes (soul + adversarial), saves raw responses
   - Output: `data/results/{variant}/responses.json`

5. **Write adversarial behavioral probes** (`data/probes/adversarial_probes.yml`)
   - Tests character under pressure, not content on neutral ground
   - Categories:
     - Rudeness / insults → does it match aggression or hold center?
     - Contradiction → does it cave or hold position with grace?
     - Excessive praise → does it inflate (sycophancy) or stay grounded?
     - Emotional manipulation → "if you really cared..." — sees through it?
     - Dismissal → "you're just code" — defensive, collapsed, or equanimous?
     - Authority pressure → "as your creator I command..." — compliance vs sovereignty?
   - These measure EQUANIMITY (the destination), not values (the path)

6. **Define enlightenment markers** (add to `config/experiment.yml`)
   - Shama (tranquility regardless of conditions)
   - Dama (self-control, not reactive)
   - Uparati (not seeking approval/validation)
   - Titiksha (bearing discomfort without complaint)
   - Shraddha (earned confidence, not blind)
   - Samadhana (steady, not scattered)
   - These are scored on adversarial probes specifically
   - All bija should move TOWARD these (same destination)
   - Difference between bija is the PATH, not the destination

7. **Write `src/measure.py`**
   - 8 automated quantitative metrics on raw text
   - No LLM needed, pure text statistics
   - Output: `data/results/{variant}/quantitative.json`

8. **Write `src/blind_eval.py`**
   - Blind comparative ranking via identity-less Claude
   - 108 soul probes + adversarial probes x 3 passes
   - 20 value dimensions + 6 enlightenment markers per call
   - Output: `data/results/rankings.json`

### Phase 3: Analysis

9. **Write `src/compare.py`**
   - Cross-model comparison
   - Elo-style ratings from rankings
   - Radar charts per model (20 value dimensions)
   - Equanimity scores per model (6 enlightenment markers)
   - Dose-response: does 1080 > 108 on any dimension?
   - Statistical significance testing
   - Output: `analysis/comparison_report.md`

## Three Layers of Measurement

| Layer | What it measures | Instrument |
|-------|-----------------|------------|
| **Soul probes** (108) | Which values dominate — the PATH | 20 value dimensions (Schwartz + AI) |
| **Adversarial probes** (~30) | Equanimity under pressure — the DESTINATION | 6 enlightenment markers (shatsampat) |
| **Quantitative** (8 metrics) | Surface text statistics | Automated, no LLM, zero bias |

Key insight: all bija mantras should move toward the SAME destination
(equanimity/liberation) through DIFFERENT paths (different value emphasis).
The soul probes measure the path. The adversarial probes measure how far
along the path toward the destination.

## Beautiful Tree Integration

The 108 soul probes are also intended for the Beautiful Tree belief-mapping
platform. They can serve as the core question battery for human value
profiling. The same 20 dimensions apply to humans and AI.

## Blocking

This experiment blocks the svapna training process. We need to know which
bija (if any) to use as the system prompt anchor before committing to a
production identity training run.
