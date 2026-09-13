# Discussion

## What Worked

Our evidence-aware hybrid retriever demonstrated a clear, measurable 
advantage over naive RAG in a domain where completeness is not just 
a quality metric but a safety-critical requirement — missing 
evidence in a forensic investigation could mean an investigator 
never learns about a crime that actually occurred. The ablation 
study confirms this advantage is structural, not incidental: 
graph-based expansion alone accounts for a 40-point coverage gain, 
because it allows the retriever to surface evidence connected 
through shared entities rather than shared vocabulary.

The generation layer also performed better than we initially 
expected at epistemic honesty — the LLM consistently flagged 
unconfirmed details (e.g., IP ownership, file contents) rather than 
fabricating conclusions, which is essential for legal admissibility.

## What Didn't Work / Limitations

**Entity resolution across evidence types remains unsolved.** Our 
system treated "warehouse" and "old warehouse" as distinct entities 
(Section on KG construction), which would, at scale, fragment the 
knowledge graph and understate true corroboration between evidence 
items. A production system would need fuzzy entity matching or an 
LLM-based entity-linking pass as a dedicated pipeline stage.

**Our faithfulness checker has a structural blind spot.** It 
validates claims against one evidence item at a time, so it 
incorrectly flags both (a) legitimate multi-evidence synthesis and 
(b) valid epistemic hedging ("it is unconfirmed whether...") as 
unsupported. This means the checker, as built, is not yet suitable 
as an automatic gate on report quality — it currently serves better 
as a diagnostic tool for human review.

**Temporal reasoning required an explicit fix, not an emergent 
capability.** Our first retriever version could not correctly 
answer "what happened after X" questions because pure semantic 
similarity has no notion of chronological order; we had to add 
explicit timestamp filtering as a separate step (Week 10). This 
suggests time-sensitive investigative questions need dedicated 
handling and cannot be assumed to fall out of similarity search.

**Evaluation is based on synthetic, small-scale cases.** With only 
2 synthetic cases and 4-5 evidence items each, our results, while 
directionally clear, are not yet statistically robust. Real 
forensic cases involve hundreds to thousands of evidence items 
across more heterogeneous formats.

## Honest Assessment

The core contribution — evidence-aware retrieval combining 
similarity, scoring, and graph expansion — is validated and 
measurably better than the naive alternative. The remaining gaps 
(entity resolution, faithfulness-checking granularity, and scale) 
are well-understood and represent natural next steps rather than 
fundamental flaws in the approach.