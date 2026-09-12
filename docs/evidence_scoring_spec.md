# Evidence Scoring Specification — Week 6 Day 2

## Formula
evidence_score = (w1 × recency_score) + (w2 × reliability_score) + (w3 × corroboration_score)

Default weights (to be tuned in Week 9): w1 = 0.3, w2 = 0.4, w3 = 0.3

## Component definitions

### Recency score
Inverse function of time-distance between evidence timestamp and the 
query's reference time window. Evidence closer to the incident time 
window scores higher.

### Reliability score
Directly uses the `confidence` field from the evidence schema (Week 5 
Day 4), reflecting source-type trustworthiness (e.g. network logs ≈ 0.85-0.95, 
self-reported chat ≈ 0.7-0.9).

### Corroboration score
Counts how many *independent* evidence items (different source_type, 
different raw_source_file) reference the same entity_refs or event. 
Higher independent corroboration = higher trust, similar to how 
investigators trust a fact more when multiple unrelated sources confirm it.

## Why this matters
This is the core mechanism that differentiates our system from generic 
RAG (which ranks purely by semantic similarity). It directly implements 
the novelty claimed in our problem statement (Week 5 Day 2).

## Pseudocode
```
def evidence_score(item, query_time, all_evidence):
    recency = 1 / (1 + abs(item.timestamp - query_time))
    reliability = item.confidence
    corroboration = count_independent_corroborating_sources(item, all_evidence) / total_sources
    return 0.3*recency + 0.4*reliability + 0.3*corroboration
```