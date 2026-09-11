# RAG Architecture — Methodology Note (Week 3 Milestone)

## 1. Overview

The system is a Retrieval-Augmented Generation (RAG) pipeline built to answer
investigator queries over heterogeneous digital-forensic evidence (chat logs,
call records, file metadata, location pings). Rather than relying on an LLM's
parametric knowledge, every answer is generated strictly from evidence retrieved
at query time, with the goal of keeping outputs traceable back to source evidence
— a requirement for legal/investigative use, not just general Q&A.

## 2. Pipeline Components

**Storage & Retrieval:** Evidence items are stored as short text documents in a
local ChromaDB vector collection. Each document is embedded and indexed for
similarity search. ChromaDB was chosen over FAISS for this stage because it
handles embedding + storage + querying in one lightweight API, which suited
fast prototyping without managing a separate embedding pipeline.

**Query Handling:** An investigator query (e.g. "What did the suspect do around
11 PM?") is embedded and matched against the evidence collection using dense
similarity search (`collection.query`, top-k=3). This returns the most
semantically relevant evidence chunks rather than requiring exact keyword
matches — important since real evidence phrasing rarely matches investigator
question phrasing exactly.

**Generation:** Retrieved chunks are concatenated into a context block and
passed to an LLM (Gemini) with an explicit instruction to answer *using only*
the provided evidence and to cite which evidence line supports the answer.
This constrains the model to grounded, citable output rather than free
generation.

**Knowledge Graph layer (parallel track):** Alongside the retrieval pipeline,
a separate knowledge-graph module (`kg_builder_v0.py`) uses NER (spaCy) plus
manual relation extraction to build entity-relationship graphs from sample
case-note text (nodes: people, devices, locations; edges: relations like
"called", "sent message to"). This is being developed as the correlation layer
that the final system will use to expand retrieval beyond pure text similarity
— e.g. pulling in evidence connected to an entity even if it doesn't
lexically match the query. This is the core "evidence-aware" novelty planned
for Phase 4.

## 3. Evaluation Approach

Faithfulness — whether a generated answer is actually supported by retrieved
context — was identified as the highest-priority metric for this use case,
since an unsupported claim in a forensic report is far more damaging than a
low-relevance answer.

A custom lightweight faithfulness check was implemented (word-overlap between
answer and retrieved context) as a stand-in for RAGAS, since RAGAS could not be
installed in the current environment (Python 3.14 lacks prebuilt wheels for
some ML dependencies; resolving this requires either downgrading to Python
3.11/3.12 or installing full C++ build tools — deferred to a later week).

**Limitation observed:** the word-overlap heuristic systematically
under-scores well-grounded answers, because it penalizes the model's own
formatting language ("Based on the evidence provided", "**Supporting
Evidence:**") and normal reasoning connectives, not just actual hallucinated
content. Manual inspection of all test cases confirmed the generated answers
were correctly grounded despite the depressed scores. This motivates moving to
a stricter, meaning-based faithfulness metric (RAGAS proper, or an NLI/entailment
based check) once the environment issue is resolved — a concrete direction for
Phase 5 (Evaluation).

## 4. Design Rationale Summary

| Choice | Reasoning |
|---|---|
| ChromaDB | Fast local setup, embedding+storage+query in one API |
| Dense retrieval only (no BM25 yet) | Sufficient for prototype; hybrid retrieval planned for Phase 4 |
| Citation-required prompting | Enforces traceability, core to "evidence-aware" claim |
| Custom faithfulness heuristic | RAGAS blocked by environment; heuristic is a temporary, documented substitute |
| Parallel KG track | Will merge with retriever in Phase 4 for graph-guided retrieval (the paper's novelty claim) |