# Coding and Experiment Conventions

> updated: 2026-07-16

- Experiment behavior is config-driven. No condition, dose, model, or spend cap
  is silently hard-coded in a runner.
- Every collection unit has a deterministic ID and append-only attempt history.
- Resuming never overwrites a prior response.
- Normalize Unicode explicitly and record code points, separator, complete-prefix
  tokenizer output, and a SHA-256 prefix hash. Isolated-unit tokenization is not
  sufficient.
- Record traditional dose and computational dose separately.
- Fail closed on count mismatch, tokenizer absence, context overflow, model-ID
  drift during a frozen run, or projected spend-cap breach.
- Keep API keys in environment variables. Never write them to config, logs,
  manifests, or errors.
- Raw runs, generated prefixes, model weights, and caches remain ignored. Commit
  configs, probe sets, schemas, analysis code, and final reports.
- Fresh conversation per probe. Never let one evaluated response condition the
  next probe.
- Preserve malformed, refused, retried, and null outputs with explicit status.
- Subject and judge models are different model families.
- Do not change confirmatory probes, outcome definitions, exclusions, or judge
  rubrics after condition labels are visible.
- Use `pathlib` for filesystem paths and UTF-8 explicitly for text artifacts.
- Keep commands non-interactive and resumable.
