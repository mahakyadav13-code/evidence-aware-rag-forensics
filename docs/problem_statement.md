# Problem Statement & Novelty — Week 5 Day 2

## Problem Statement
Digital forensic investigations require correlating evidence across 
heterogeneous sources — chat logs, network traffic, file metadata, 
call records — to reconstruct timelines and relationships between 
entities. This correlation is currently performed manually by 
investigators, as demonstrated in real cases such as the DFRWS 2011 
Android forensic challenge, where distinguishing a perpetrator from 
an unknowing victim required cross-referencing SMS, browsing history, 
and file activity by hand. Existing AI-assisted approaches address 
parts of this problem in isolation: RAG-based systems (e.g. GenDFIR, 
ForensicLLM) improve retrieval and generation but do not incorporate 
evidentiary properties like source reliability or corroboration into 
retrieval; knowledge-graph-based systems (e.g. DFKG, FEAR) model 
relationships between artifacts but lack generative reasoning or 
natural-language reporting. No existing system combines evidence-aware 
retrieval, cross-source correlation, and citation-verified generation 
into a single automated pipeline suitable for investigator use.

## Novelty
We introduce an Evidence-Aware Retrieval-Augmented Generation (RAG) 
framework that:
1. Scores retrieved evidence chunks using forensic-relevant factors 
   (recency, source reliability, corroboration across sources) rather 
   than semantic similarity alone.
2. Builds a knowledge graph linking entities, devices, and timestamps 
   across heterogeneous evidence types to support multi-hop 
   correlation queries.
3. Generates investigator-readable reports where every claim is 
   traceable to a specific evidence ID, addressing the admissibility 
   and provenance requirements identified in Week 4.

This combination — evidence-aware scoring + graph-guided correlation + 
citation-verified generation — has not been jointly addressed in prior 
work (see literature review, Week 5 Day 1), constituting the core 
contribution of this project.