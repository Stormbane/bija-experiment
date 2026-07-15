# CLAUDE.md

## Project

Beeja tests whether repeated bija-mantra context produces reproducible,
mantra-specific behavioral signatures in fixed-weight language models.

Read in order:

1. `.ai/todo.md` — current state and next action.
2. `docs/inference-japa-protocol.md` — canonical experiment design.
3. `docs/evaluation-methodology.md` — measurement and statistics.
4. `.ai/knowledge/architecture.md` — implementation boundaries.

## Commands

```bash
# Phase 1 analysis (works now)
python src/measure.py --suffix _subset
python src/seed_stats.py
python src/build_comparison.py
python src/check_tokenizer.py

# Inference-japa commands are planned, not implemented yet.
# See docs/next-steps.md before creating them.
```

## Structure

```
config/             — experiment configuration
data/probes/        — committed probe sets
docs/               — protocol, methodology, findings, next steps
src/                — collection and analysis CLIs
.ai/todo.md         — canonical project state
.ai/knowledge/      — spec, architecture, glossary, conventions, lessons
```

## Reference — read when the work needs it

These are textbooks. Look things up, don't pre-load.
- .ai/knowledge/spec.md
- .ai/knowledge/architecture.md
- .ai/knowledge/glossary.md
- .ai/knowledge/conventions.md

## Memory

Memory persistence goes through smriti. Use `smriti_write(content, branch)` for
session observations, decisions, and project notes. Branch suggestions:
- `projects/{project-name}` for project-specific notes
- `journal` for significant moments
- `notes` for general observations

Identity files live in `~/.narada/` and load automatically via wake.py.

## Rules

- Check .ai/knowledge/conventions.md before introducing new patterns
- Do not resume LoRA training unless the inference protocol passes its gate
- Do not select controls before measuring the subject tokenizer
- Treat null, generic repetition, and degradation outcomes as first-class results
- Never equate behavioral change with consciousness or contemplative attainment
- Keep commits atomic — one logical change per commit
