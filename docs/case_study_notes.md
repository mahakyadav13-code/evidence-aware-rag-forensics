# Case Study Notes — DFRWS 2011 Forensic Challenge (Android)

Source: DFRWS 2011 Forensics Challenge (dfrws.org), summarized via
secondary analysis write-up.

## Scenario

Two linked investigations, each requiring analysis of an Android
device:
1. Donald Norby found dead (unclear suicide/homicide); investigators
   examined his device to reconstruct who he communicated with prior
   to death, and his possible ties to a criminal group.
2. Yob Toag's device was examined for evidence of intellectual
   property theft (leak of confidential company documents).

## How investigators manually correlated evidence

No single evidence source was sufficient. Investigators had to
cross-reference:
- SMS messages
- Contact records
- Browsing history
- Emails
- File downloads
- File system artifacts (timestamps, file metadata)

By manually lining these up chronologically and cross-referencing
entities (who texted whom, when a file was downloaded relative to a
message, when a browser search happened relative to a call), they
reconstructed a coherent timeline and relationship map across both
devices.

## Outcome

The correlated evidence showed Donald Norby had orchestrated the
theft and attempted sale of confidential documents, while Yob Toag
was an unknowing victim of a malware compromise — a conclusion only
reachable by combining evidence types, not from any single artifact
type alone.

## Relevance to our project

This case is a real-world example of exactly the manual correlation
work our evidence-aware RAG + knowledge-graph system is designed to
automate:
- Multiple heterogeneous evidence types (chat, file metadata,
  browsing/network activity) → matches our evidence schema (Week 5).
- Cross-referencing entities and timestamps by hand → this is the
  correlation-engine / graph-guided retrieval task planned for
  Phase 4.
- Distinguishing an intentional actor from an unknowing victim
  required combining timeline + relationship evidence — this is a
  strong justification for why single-document retrieval (plain RAG)
  is insufficient, and why our graph-guided, evidence-aware approach
  is the correct architecture for this domain.

Source: https://bilyaminu1.medium.com/android-forensic-analysis-dfrws-2011-forensic-challenge-b74e18a192d7
Original challenge: http://old.dfrws.org/2011/challenge/index.shtml