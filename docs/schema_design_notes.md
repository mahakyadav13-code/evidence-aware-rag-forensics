# Evidence Schema Design Notes — Week 5 Day 4

## Why this schema

Our evidence-aware RAG system needs a **single common structure** across 
every heterogeneous evidence type (chat logs, call logs, file metadata, 
network logs, location pings) so the retriever, correlation engine, and 
generator can all operate on evidence uniformly, regardless of its 
original source format.

## Field-by-field rationale

- **evidence_id**: A stable, unique reference for every piece of evidence. 
  This is what the generation layer (Week 11) will cite in every claim it 
  makes, so investigators can trace any generated statement back to its 
  exact source — directly addressing the admissibility/provenance 
  requirement identified in Week 4 Day 4.

- **source_type**: Lets the correlation engine and retriever apply 
  type-specific logic later (e.g. weighting a call log differently from 
  a location ping) and lets us report evidence-type coverage in our 
  evaluation (Week 13).

- **timestamp**: Normalized to ISO 8601 so evidence from different raw 
  formats (which log time differently) can be placed on one unified 
  timeline — this is the foundation of the Timeline Builder module 
  (Week 10).

- **entity_refs**: Normalized IDs (e.g. `PERSON-John`, not raw phone 
  numbers or usernames) so the same person/device is recognized 
  consistently across all evidence sources. This is what makes 
  knowledge-graph construction (Week 8) possible — without normalized 
  entity IDs, the same person could appear as three different "nodes."

- **content**: The actual evidence text/description that gets embedded 
  and retrieved. This is the field the vector DB indexes for semantic 
  search.

- **confidence**: A source-reliability score between 0 and 1. This is 
  the core input to our evidence-aware scoring function (Week 9) — it's 
  what distinguishes our retriever from a generic RAG system that treats 
  all retrieved text as equally trustworthy.

- **raw_source_file**: A pointer back to the original raw file. This 
  preserves chain-of-custody traceability (Week 4 Day 4) — even after 
  normalization and embedding, we can always prove exactly where a 
  piece of evidence physically came from.

## Design principle

Every field exists to serve one of three goals: (1) enabling retrieval, 
(2) enabling correlation across sources, or (3) enabling legal 
traceability. If a future field doesn't clearly serve one of these 
three purposes, it shouldn't be added to the schema.