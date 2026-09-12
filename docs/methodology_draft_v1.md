# Methodology Draft v1 — Week 6 Day 6

This document consolidates the system design completed in Week 6 into 
a single methodology reference, to be refined into the paper's 
Methodology section in Week 15.

## 1. System Overview
See `architecture_overview.md` — 6-stage pipeline: Ingestion → 
Normalization → Correlation Engine (KG) → Evidence-Aware Retriever → 
Generator → Investigator Report. Every stage preserves `evidence_id` 
and `raw_source_file` end to end, ensuring full traceability from raw 
evidence to final report.

## 2. Evidence Scoring
See `evidence_scoring_spec.md` — evidence is ranked using a weighted 
combination of three factors rather than semantic similarity alone:

evidence_score = (0.3 × recency_score) + (0.4 × reliability_score) + (0.3 × corroboration_score)


- Recency: closeness of evidence timestamp to the query's time window
- Reliability: the `confidence` field from the evidence schema
- Corroboration: how many independent sources support the same event/entity

## 3. Knowledge Graph Schema
See `kg_schema_spec.md` — defines the correlation engine's structure:

**Node types:** Person, Device, IP, Location, Event
**Edge types:** COMMUNICATED_WITH, OWNS, USED, LOCATED_AT, 
PARTICIPATED_IN, FOLLOWED_BY

This schema is what the correlation engine (Week 8) builds from 
extracted entities/relations, and what the retriever (Week 9) traverses 
for graph-guided expansion.

## 4. Evidence-Aware Retrieval
See `retriever_pseudocode.md` — a hybrid ranking function combining 
three signals:

final_score = (0.4 × dense_similarity) + (0.35 × evidence_score) + (0.25 × graph_proximity_score)


Graph proximity allows retrieval of evidence connected to query 
entities even without keyword or embedding overlap — the key advantage 
over generic RAG.

## 5. Generation & Citation
See `generation_prompt_design.md` — the generator is constrained by a 
prompt template requiring every claim to cite a specific `evidence_id` 
in `[EVID-XXXX]` format, include a Confidence Level based on 
corroboration, and explicitly decline to answer when evidence is 
insufficient — directly addressing the admissibility requirements 
identified in Week 4 Day 4.

## Status
Architecture design is complete and internally consistent — each 
module clearly consumes/produces data conforming to the evidence 
schema (Week 5 Day 4). Ready to begin implementation (Phase 4, Week 7).

## Module Ownership — Phase 4

| Week | Module | Owner |
|---|---|---|
| 7 | Ingestion + Normalization | [Person A / Person B] |
| 8 | Entity/Relation Extraction + KG Builder | [Person A / Person B] |
| 9 | Evidence-Aware Retriever | [Person A / Person B] |
| 10 | Correlation Engine (multi-hop) | [Person A / Person B] |
| 11 | Generator | [Person A / Person B] |
| 12 | UI + Integration | [Both] |

(Fill in actual names based on your Appendix A role split from the 
original 16-week roadmap.)