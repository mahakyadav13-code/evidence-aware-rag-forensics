# Generation Strategy Design — Week 6 Day 5

## Prompt template

SYSTEM INSTRUCTION:
You are assisting a digital forensic investigator. You will be given a
set of retrieved evidence items, each with a unique evidence_id. Answer
the investigator's question using ONLY the evidence provided. Every
factual claim in your answer MUST cite the evidence_id(s) that support
it, in the format [EVID-XXXX]. If the evidence does not support a
confident conclusion, say so explicitly rather than guessing.

EVIDENCE:
[EVID-0001] John called Mike. Call lasted 14 minutes. (2026-03-05T22:30:00)
[EVID-0004] Mike sent a message to John: 'meet me at the warehouse'. (2026-03-05T22:35:00)
[EVID-0002] File 'transfer.zip' created on John's laptop. (2026-03-05T22:52:00)
...

INVESTIGATOR QUESTION:
{query}

OUTPUT FORMAT:

Summary (2-3 sentences)
Supporting Evidence (bulleted, each with evidence_id citation)
Confidence Level (High / Medium / Low, based on corroboration)

## Output format requirements
1. Every claim must include at least one `[EVID-XXXX]` citation
2. No entity or event may be mentioned unless it appears in the provided evidence
3. A "Confidence Level" field forces the model to reflect corroboration 
   strength rather than presenting all claims as equally certain
4. If evidence is insufficient, the model must say so rather than 
   inferring beyond what's given

## Why this design
This directly implements the citation-traceability requirement from our 
problem statement (Week 5 Day 2) and legal/admissibility analysis 
(Week 4 Day 4) — output must be auditable back to source evidence, not 
just fluent-sounding text.

## Next step
This template gets implemented as real code in `generator/report_gen.py` 
(Week 11), paired with a post-generation citation-verification check.