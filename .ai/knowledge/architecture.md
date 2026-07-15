# Architecture

> updated: 2026-07-16

## Tech Stack

- Python command-line pipeline.
- YAML experiment and probe configuration.
- JSON/JSONL append-only run artifacts.
- DeepSeek's OpenAI-compatible API for the primary inference study.
- Official subject-model tokenizer for prefix measurement.
- Statistical analysis with a pinned Python stack; exact packages selected in
  Phase A.
- Legacy local stack: Qwen3-8B, Unsloth, PyTorch, PEFT/LoRA.

## Project Structure

```text
config/                 experiment definitions and hard spend caps
data/probes/            committed probe sets
data/inference-japa/    ignored raw run artifacts, organized by run ID
data/results/           ignored Phase 1 outputs
data/research/          local mantra research corpus
docs/                   protocol, methodology, findings, next actions
models/                 ignored Phase 1 LoRA adapters
src/                    generation, collection, validation, and analysis CLIs
.ai/                    compact project state and knowledge
```

Large prefixes and raw responses are ignored. Small configs, schemas, probes,
analysis code, and final reports are committed.

## Data Flow

```text
experiment config
    -> tokenizer + Unicode audit
    -> exact japa prefixes + hashes + token counts
    -> dry-run cost/context validation
    -> independent API request per condition × dose × probe × replicate
    -> append-only responses.jsonl + manifest metadata
    -> deterministic integrity and surface metrics
    -> blind randomized comparative evaluation
    -> frozen statistical analysis
    -> report with positive/generic/degraded/null interpretation
```

The japa prefix is reused across independent probe requests so provider prefix
caching can operate without allowing responses to contaminate later probes.

## API Design

The subject adapter targets an OpenAI-compatible chat-completions interface.
Every request uses:

- one fixed neutral system message;
- one condition-specific assistant-role japa prefix, omitted for baseline;
- one user probe;
- fixed non-thinking generation settings.

The client records the requested and returned model IDs, request ID, timestamps,
latency, input/output/cache tokens, estimated cost, retry history, and terminal
status. A deterministic unit ID makes collection resumable without overwriting
attempts.

Provider-specific code stays behind a small adapter. Experiment logic must not
depend on undocumented DeepSeek behavior.

## Planned Commands

```bash
python src/build_japa_prefixes.py --config config/inference-japa.yml
python src/run_inference_japa.py --config config/inference-japa.yml --dry-run
python src/run_inference_japa.py --config config/inference-japa.yml
python src/validate_inference_japa.py --run-id <run-id>
python src/analyze_inference_japa.py --run-id <run-id>
```

These are architectural targets, not claims that the scripts already exist.
