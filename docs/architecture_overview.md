# Full System Architecture — Week 6 Day 1

## Pipeline stages
1. **Ingestion** — parses each raw evidence type (chat, call, file, network, 
   location) into the common schema (Week 5 Day 4).
2. **Normalization** — standardizes timestamps to ISO 8601 and resolves 
   entity references to consistent IDs across sources.
3. **Correlation Engine** — builds a knowledge graph linking entities, 
   devices, and timestamps (Week 8), enabling multi-hop reasoning.
4. **Evidence-Aware Retriever** — combines dense + BM25 retrieval with 
   evidence scoring (recency, reliability, corroboration) and graph-based 
   expansion (Week 9).
5. **Generator** — produces investigator-readable reports where every 
   claim cites a specific evidence ID (Week 11).
6. **Output** — a traceable, admissibility-conscious investigator report.

## Design principle
Every stage preserves the evidence_id and raw_source_file link from 
ingestion through to the final report, ensuring end-to-end traceability 
as required by our Week 4 legal/admissibility analysis.