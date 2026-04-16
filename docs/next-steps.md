# Next Steps

Pick up from here in the next session on this directory.

## TODO (in order)

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

4. **Write `src/run_eval.py`**
   - Loads each model, runs 108 soul probes, saves raw responses
   - Output: `data/results/{variant}/responses.json`

5. **Write `src/measure.py`**
   - 8 automated quantitative metrics on raw text
   - No LLM needed, pure text statistics
   - Output: `data/results/{variant}/quantitative.json`

6. **Write `src/blind_eval.py`**
   - Blind comparative ranking via identity-less Claude
   - 108 probes x 3 passes = 324 evaluator calls
   - 20 value dimensions per call
   - Output: `data/results/rankings.json`

7. **Write `src/compare.py`**
   - Cross-model comparison
   - Elo-style ratings from rankings
   - Radar charts per model (20 dimensions)
   - Statistical significance testing
   - Output: `analysis/comparison_report.md`

## Key Design Decisions

- System prompt = bija only (no English identity text)
- Training content identical across variants (controls for content)
- Evaluation is blind (evaluator doesn't know which model is which)
- Comparative ranking, not absolute scoring (more reliable)
- 3 evaluation passes for inter-rater reliability
- Both Schwartz (validated psychology) and AI-specific dimensions (20 total)

## Beautiful Tree Integration

The 108 soul probes are also intended for the Beautiful Tree belief-mapping
platform. They can serve as the core question battery for human value
profiling. The same 20 dimensions apply to humans and AI.

## Blocking

This experiment blocks the svapna training process. We need to know which
bija (if any) to use as the system prompt anchor before committing to a
production identity training run.
