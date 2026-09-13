# Results

## 4.1 Evidence Coverage: Hybrid vs Naive Baseline

We compared our evidence-aware hybrid retriever against a naive 
baseline (plain dense retrieval, top-3 chunks, no scoring or graph 
expansion) across two synthetic cases. Table 1 and Figure 1 
summarize the results.

| Case | Hybrid System | Naive Baseline |
|------|---------------|-----------------|
| Case v0 (5 evidence items) | 100.0% | 60.0% |
| Case v1 (4 evidence items) | 100.0% | 75.0% |

The hybrid system achieved complete evidence coverage on both test 
cases, while the naive baseline consistently missed 25-40% of 
relevant evidence. Critically, in Case v0, the naive baseline 
omitted the file-creation and file-upload evidence — the two pieces 
of evidence documenting the actual act of data exfiltration — while 
surfacing only communication and location evidence. This suggests 
that pure semantic similarity retrieval, when limited to a small 
top-k, is prone to missing evidence that is causally central to a 
case but not textually similar to a natural-language query.

## 4.2 Ablation Study

To isolate the contribution of each component in our hybrid 
retriever, we evaluated three configurations on Case v0: (1) the 
full system, (2) the system with graph-based expansion removed, 
and (3) the system with evidence-aware scoring removed. Results 
are shown in Table 2 and Figure 2.

| Configuration | Evidence Coverage |
|---------------|-------------------|
| Full hybrid system | 100.0% |
| No graph expansion | 60.0% |
| No evidence scoring | 80.0% |

Removing graph-based expansion produced the largest performance 
drop (40 percentage points), indicating that cross-referencing 
entities across evidence items — rather than relying on similarity 
alone — is the primary driver of our system's completeness 
advantage over naive RAG. Removing evidence-aware scoring produced 
a smaller but still meaningful drop (20 percentage points), 
suggesting recency/reliability/corroboration weighting helps 
surface additional relevant evidence, though to a lesser degree 
than graph expansion.

## 4.3 Qualitative Observations

[Insert Week 11 Day 4 faithfulness-check findings and Week 8 
entity-resolution findings here as sub-sections, since these are 
also results worth reporting, not just discussion points.]