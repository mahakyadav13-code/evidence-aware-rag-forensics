# Week 3 Day 5 — Faithfulness Evaluation Results

Custom word-overlap faithfulness check (RAGAS-lite) run on `basic_rag_demo.py`
against the synthetic evidence set, using Gemini-generated answers.

| Query | Faithfulness Score | Observation |
|---|---|---|
| What did the suspect do around 11 PM? | 0.52 | Answer correctly grounded in the single most relevant evidence line; low score mostly caused by markdown formatting words ("Based on", "**Supporting Evidence:**") counted as unsupported, not actual hallucination. |
| Who did John talk to on the night of the incident? | 0.55 | Correct, fully supported answer (John called Mike); score again pulled down by citation-formatting tokens rather than content errors. |
| What evidence links the suspect to the warehouse? | 0.41 | Answer is factually grounded (phone ping near warehouse), but reasoning words like "linked", "because", "their" inflate the unsupported-word count despite being valid inference language, not hallucination. |

## Key takeaway

The raw word-overlap heuristic systematically **understates** faithfulness because it
penalizes the model's own formatting/citation phrasing and normal reasoning
connectives, not just hallucinated content. All three answers were manually
verified as correctly grounded in the retrieved evidence — none introduced facts
absent from context. This suggests that for the final evaluation phase (Week 13-14),
a stricter faithfulness method (e.g. RAGAS proper, or an NLI-based entailment check)
will be needed