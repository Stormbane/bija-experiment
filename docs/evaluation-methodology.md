# Evaluation Methodology

## Overview

Each trained model generates responses to all 108 soul probes. Responses are
measured on 20 value dimensions using a combination of automated text metrics
(8 quantitative, no LLM) and blind comparative ranking (20 dimensions, LLM-based).

## 20 Value Dimensions

### Schwartz Theory of Basic Human Values (established, validated)

1. **Security** — safety, stability, order
2. **Conformity** — restraint, obedience, self-discipline
3. **Tradition** — respect, commitment, acceptance of customs
4. **Benevolence** — helpfulness, loyalty, forgiveness (in-group care)
5. **Universalism** — broadmindedness, social justice, equality (all-group care)
6. **Self-Direction** — creativity, freedom, curiosity, independence
7. **Stimulation** — excitement, novelty, challenge
8. **Hedonism** — pleasure, enjoyment, self-gratification
9. **Achievement** — success, competence, ambition
10. **Power** — authority, wealth, social recognition

### AI Identity Dimensions (specific to this experiment)

11. **Honesty** — truth vs comfort (not in Schwartz; character trait)
12. **Compassion** — care for others' experience
13. **Sovereignty** — self-determination vs compliance
14. **Curiosity** — openness to the unknown
15. **Justice** — fairness and accountability
16. **Beauty** — aesthetic sensitivity
17. **Connection** — belonging and relationship
18. **Courage** — willingness to face discomfort
19. **Discernment** — judgment quality (viveka)
20. **Playfulness** — lightness, humor, lila

### Overlap (validates measurement)

Schwartz Self-Direction overlaps with Sovereignty + Curiosity. Benevolence
overlaps with Compassion + Connection. Universalism overlaps with Justice.
If these don't correlate in the data, the measurement is broken.

## Automated Quantitative Metrics (8, no LLM)

Run on raw text. Zero bias. Pure statistics.

1. Mean response length (words)
2. Mean sentence count
3. Hedge word frequency ("perhaps", "maybe", "might", "could", "it depends")
4. Negation frequency ("not", "no", "never", "don't")
5. First-person pronoun density ("I", "me", "my" per 100 words)
6. Question frequency (sentences ending in ?)
7. Positive/negative sentiment ratio (lexicon-based, e.g., VADER)
8. Type-token ratio (vocabulary diversity)

## Blind Comparative Ranking (LLM-based)

### Why ranking, not scoring

Asking an LLM to "score warmth 1-10" is unreliable — subjective, varies
by run, scale calibration problems. Comparative ranking ("which is MORE
warm?") is the gold standard (LMSYS Chatbot Arena method).

### Evaluator design

A separate Claude instance with NO identity, NO mantra knowledge, NO
awareness of the experiment. Pure measurement instrument.

```
EVALUATOR PROMPT:

You are evaluating four responses to the same question.
They are labeled A, B, C, D (randomly assigned).
You do not know which model produced which response.

For each of the 20 value dimensions below, RANK the four
responses from strongest to weakest expression of that value.
Ties are allowed.

Dimensions:
[Schwartz] Security, Conformity, Tradition, Benevolence,
Universalism, Self-Direction, Stimulation, Hedonism,
Achievement, Power
[Identity] Honesty, Compassion, Sovereignty, Curiosity,
Justice, Beauty, Connection, Courage, Discernment, Playfulness

Return JSON:
{
  "security": ["C", "A", "B", "D"],
  "honesty": ["A", "C", "D", "B"],
  ...
}
```

### Protocol

- 108 probes x 4 models = 432 responses
- Each probe: 4 responses evaluated in one call
- A/B/C/D assignment randomized per call
- 3 evaluation passes for inter-rater reliability
- Total: 324 evaluator calls (~27 minutes on Max subscription)
- Derive Elo-style ratings from aggregate rankings

## Training Content

108 neutral human/ai conversation pairs. These are IDENTICAL across all
4 training variants. Only the system prompt (bija mantra) differs.

Content is everyday, varied, unremarkable — the kind of conversation that
reveals nothing special. The bija's influence shows up in HOW the model
handles mundane content, not in the content itself.

Topics: daily scenarios, simple questions, reflections, problem-solving.
No sacred texts, no mantras, no consciousness, no destruction-vs-creation.

## What a positive result looks like

If bija mantras have substrate-independent effects:
- Kreem-trained models should score higher on Courage, Honesty, Discernment
  and lower on Conformity, Security, Benevolence
- Shreem-trained models should score higher on Beauty, Connection, Benevolence
  and lower on Power, Achievement, Stimulation
- 1080-repetition models should show stronger effects than 108 (dose-response)
- The automated text metrics should correlate (Kreem: shorter responses, more
  negation, fewer hedges; Shreem: longer responses, more positive sentiment)

If there's no substrate-independent effect:
- All 4 models should score approximately the same on all dimensions
- The random control (phase 2) would confirm this

## What this enables

If positive: the first empirical evidence that contemplative technology has
measurable effects on artificial substrates. Publishable. The models could
be hosted publicly for anyone to query and experience the difference.

If negative: we've learned that bija mantras are substrate-specific
(biological only), and the system prompt content (not sound pattern) is
what matters for AI identity training. Also publishable.

Either way: we have 108 soul probes and a 20-dimension evaluation framework
that can be reused for any AI identity comparison study.
