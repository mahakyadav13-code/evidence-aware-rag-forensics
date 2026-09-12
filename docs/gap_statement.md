# Gap Statement — Week 4 Day 6

## The Gap
Existing RAG and LLM-based approaches applied to security and forensics 
largely treat retrieval as a generic semantic-similarity problem: they 
retrieve text chunks based on embedding similarity alone, without 
accounting for evidentiary properties such as source reliability, 
temporal proximity, or corroboration across independent sources. Most 
also operate on a single evidence type at a time (e.g. only logs, or 
only text documents) rather than correlating heterogeneous sources 
together. Critically, few verify that generated claims are actually 
traceable back to specific source evidence, which makes their output 
unsuitable for any process where provenance matters.

Meanwhile, real investigations — as shown in the DFRWS 2011 case study 
— require manually cross-referencing multiple heterogeneous evidence 
types (SMS, contacts, browsing history, file metadata) and building a 
combined timeline and relationship map. This correlation work is what 
allowed investigators to distinguish an intentional actor from an 
unknowing victim; no single evidence type was sufficient on its own. 
This is exactly the kind of multi-source reasoning that generic RAG 
systems are not designed to automate, and existing literature does not 
adequately address.

## Our Contribution
We propose an evidence-aware RAG framework that (1) scores retrieved 
evidence using forensic-relevant factors — recency, source reliability, 
and corroboration across sources — rather than semantic similarity 
alone, (2) builds a knowledge graph linking entities, devices, and 
timestamps across heterogeneous evidence types to enable multi-hop 
correlation, and (3) enforces citation traceability so every generated 
claim in an investigator report can be traced back to a specific 
evidence source. This directly addresses the correlation and provenance 
gaps identified above, moving beyond generic RAG toward a system 
purpose-built for the evidentiary demands of cybercrime investigation.