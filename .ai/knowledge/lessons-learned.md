# Lessons Learned

## 2026-07-16 — A directional single-seed result is not a signal

The first Kreem/Shreem comparison matched the expected direction on sentiment
and decisiveness. Three-seed Kreem, Shreem, and `xyz` controls put every one of
the eight surface differences inside seed variance. Expected direction made the
first result easier to believe, not more reliable.

Applies to: every behavioral comparison. Replication and controls precede
interpretation.

## 2026-07-16 — Training and inference must not share the treatment

Phase 1 evaluated each mantra-trained adapter with the same mantra repeated
again in its system prompt. The resulting difference from base could not be
assigned to weights, active context, or their interaction.

Applies to: isolate one causal intervention per experiment. The inference-japa
study fixes weights.

## 2026-07-16 — Tokenize the complete repeated intervention

Isolated Kreem and Shreem were each four Qwen tokens and differed only in their
first token. Yet the actual space-separated 108 prefixes were 432 and 539
tokens; `xyz` was 108. A plain-space boundary merged differently with the two
initial consonants. Newline separation restored sacred-pair parity at 539/539.
Context length and separator choice are both treatments.

Applies to: inspect complete prefixes at every dose, record traditional and
computational dose, and select controls and separators from subject-tokenizer
evidence.

## 2026-07-16 — Integrity loss is not contemplative depth

Very long repetitive contexts may reduce branching, shorten answers, or damage
instruction-following. Those effects are scientifically interesting but cannot
be interpreted as silence, ego loss, concentration, or samadhi without
independent evidence.

Applies to: score behavioral integrity before value or equanimity outcomes.
