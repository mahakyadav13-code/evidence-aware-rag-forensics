# Evaluation Plan — Week 13

## Metrics to measure

1. **Retrieval Precision/Recall**
   For a given query, what fraction of retrieved evidence is actually 
   relevant (precision), and what fraction of all relevant evidence 
   was retrieved (recall)? Measured against manually-labeled 
   relevant evidence per test query.

2. **KG Accuracy vs Ground Truth**
   Compare extracted entities/relations (Week 8) against the 
   ground_truth.md timeline and events. Count correct vs missed vs 
   incorrect (hallucinated) entities/relations.

3. **Faithfulness Rate**
   Percentage of report claims that are SUPPORTED by cited evidence 
   (using the Week 11 Day 4 faithfulness checker, applied to the 
   full report rather than isolated single-evidence claims — 
   addressing the limitation found in Week 11).

4. **Citation Validity Rate**
   Percentage of citations in generated reports that reference real, 
   existing evidence IDs (from Week 11 Day 3 citation_check.py).

## Comparison baseline
Our hybrid evidence-aware retriever vs a naive baseline (plain dense 
retrieval only, no scoring/graph expansion) — see Week 13 Day 3.

## Test cases
Currently have 1 synthetic case. Week 13 Day 2 will expand to 3-5 
cases for statistical validity.