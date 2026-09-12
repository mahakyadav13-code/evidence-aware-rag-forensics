# Literature Review — Week 4 Day 5

## Paper 1
**Title:** [paper title]
**Link:** [URL]
**Method:** [1-2 sentences: what approach they used]
**Gap:** [what's missing / what they don't address]

## Paper 2
**Title:** 
**Link:** 
**Method:** 
**Gap:** 

## Paper 3
**Title:** 
**Link:** 
**Method:** 
**Gap:** 

## Paper 4
**Title:** 
**Link:** 
**Method:** 
**Gap:** 

## Paper 5
**Title:** 
**Link:** 
**Method:** 
**Gap:**

# Literature Review — Weeks 4-5

## Paper 1
**Title:** LLMs: Prompt Engineering and Retrieval Augmented Generation for Digital Forensics
**Link:** https://dfrws.org/presentation/llms-prompt-engineering-and-retrieval-augmented-generation/
**Method:** Explores prompt engineering and RAG applied to digital forensics, comparing an open-source LLM against ChatGPT on forensic tasks.
**Gap:** Focuses on prompting/RAG basics for forensics broadly; does not address evidence-aware scoring, multi-source correlation, or citation traceability.

## Paper 2
**Title:** Exploring the Potential of Large Language Models for Improving Digital Forensic Investigation Efficiency
**Link:** https://arxiv.org/pdf/2402.19366
**Method:** Surveys how LLMs (including RAG) can reduce hallucination and improve currency of forensic knowledge by retrieving from external sources.
**Gap:** General survey of LLM use in forensics; doesn't propose a specific evidence-scoring or graph-guided retrieval mechanism.

## Paper 3
**Title:** ForensicLLM: A Local Large Language Model for Digital Forensics
**Link:** https://www.sciencedirect.com/science/article/pii/S2666281725000113
**Method:** Fine-tunes a local LLM specifically for digital forensics using a Retrieval-Augmented Fine-Tuning (RAFT) approach.
**Gap:** Fine-tuning-based, not retrieval/correlation-based; doesn't handle multi-source evidence correlation or citation verification.

## Paper 4
**Title:** GenDFIR: Advancing Cyber Incident Timeline Analysis Through Retrieval-Augmented Generation and Large Language Models
**Link:** https://arxiv.org/pdf/2409.02572
**Method:** Uses RAG + LLMs to reconstruct cyber incident timelines from artefacts, timestamps, and metadata for DFIR investigations.
**Gap:** Focused specifically on timeline reconstruction from single-domain artefacts; doesn't build a full knowledge graph across heterogeneous evidence types or score evidence reliability.

## Paper 5
**Title:** Visualizing and Reasoning about Presentable Digital Forensic Evidence (DFKG)
**Link:** https://ieeexplore.ieee.org/document/9851972/
**Method:** Introduces a Digital Forensic Knowledge Graph (DFKG) capturing case background, timeline, and verifiable evidence for presentation in court.
**Gap:** Knowledge-graph based but not RAG-integrated; doesn't use LLM generation or retrieval scoring — purely a visualization/reasoning structure.

## Paper 6
**Title:** A Unified Knowledge Graph to Permit Interoperability of Heterogeneous Digital Evidence
**Link:** https://arxiv.org/pdf/2402.13746
**Method:** Proposes a unified KG/ontology approach to integrate heterogeneous evidence types (building on prior DESO and SADFC ontology work).
**Gap:** Notes prior systems (DESO, SADFC) struggle with seamless integration of large-scale heterogeneous data without human intervention — exactly the automation gap our project targets.

## Paper 7
**Title:** Evaluating the Reliability of Digital Forensic Evidence Discovered by Large Language Model: A Case Study
**Link:** https://arxiv.org/pdf/2602.20202
**Method:** Combines LLM-driven artifact extraction/refinement with a Digital Forensic Knowledge Graph (DFKG) for validation, using deterministic UIDs for traceability.
**Gap:** Closest existing work to our idea — combines LLM + KG + traceability — but is framed as a reliability-evaluation framework, not a generative evidence-aware RAG system for producing investigator reports.

## Paper 8
**Title:** FEAR: A Novel Framework for Representing Digital Forensic Artifacts (GFEAR)
**Link:** https://dl.acm.org/doi/10.1145/3712716.3712726
**Method:** Provides a domain-specific declarative language to map extracted forensic artifacts into knowledge graphs, integrating with industry tools.
**Gap:** Infrastructure/representation-focused; no retrieval-augmented generation or LLM reasoning layer.

## Paper 9
**Title:** Using Graph Database for Evidence Correlation on Android Smartphones
**Link:** https://www.researchgate.net/publication/309365257_Using_Graph_Database_for_Evidence_Correlation_on_Android_Smartphones
**Method:** Uses a graph database to correlate extracted mobile evidence and speed up investigation via graph queries.
**Gap:** Query-based graph correlation only, no natural-language generation, no LLM/RAG component, and single-device scope.

## Paper 10
**Title:** A Complete Formalized Knowledge Representation Model for Advanced Digital Forensics Timeline Analysis
**Link:** https://arxiv.org/pdf/1903.01396
**Method:** Formal ontology-based model for timeline analysis and provenance of timestamps across digital evidence.
**Gap:** Pre-LLM, purely formal/ontology-based; no learned retrieval or generative reasoning — useful for provenance concepts but not an automation pipeline.

---

## Grouped by Approach

### Fine-tuning based
- ForensicLLM (Paper 3)

### RAG based
- LLMs: Prompt Engineering and RAG for Digital Forensics (Paper 1)
- Exploring the Potential of LLMs for Digital Forensic Efficiency (Paper 2)
- GenDFIR (Paper 4)

### Knowledge-graph based
- DFKG — Visualizing and Reasoning about Presentable Evidence (Paper 5)
- Unified KG for Heterogeneous Digital Evidence (Paper 6)
- Evaluating Reliability of LLM-Discovered Evidence via DFKG (Paper 7)
- FEAR / GFEAR (Paper 8)
- Graph Database for Android Evidence Correlation (Paper 9)

### Rule-based / formal / traditional
- Formalized Knowledge Representation for Timeline Analysis (Paper 10)

---

## Key Takeaway
Paper 7 is the closest prior work — it combines LLMs with a knowledge graph and traceability (UIDs). However, it is framed as an evidence-*reliability evaluation* tool, not a generative, evidence-*aware retrieval* system that scores evidence (recency/reliability/corroboration), performs graph-guided multi-hop retrieval, and generates cited investigator reports. This gap is what our project directly targets.