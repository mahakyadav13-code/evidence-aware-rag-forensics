# Digital Forensics Process — Overview

## The 4-Phase Process

Identification → Preservation → Analysis → Presentation

1. **Identification**
   - Determine what data is potential evidence and where it lives
     (devices, cloud accounts, server logs, chat exports).
   - No data is touched yet — this phase is about scoping the
     investigation.

2. **Preservation**
   - Create exact, unaltered copies of evidence (forensic imaging).
   - Generate hashes (MD5/SHA) to prove the copy matches the original
     and hasn't been tampered with.
   - This is the technical foundation of chain of custody.

3. **Analysis**
   - Work only on the preserved copy, never the original.
   - Build timelines, correlate entities across sources (who talked to
     whom, when a file was created, where a device was located).
   - This is where our RAG + knowledge-graph system fits — assisting
     the correlation and timeline-building step.

4. **Presentation**
   - Summarize findings into a report suitable for legal/investigative
     review.
   - Every claim must be traceable to specific evidence — no
     unsupported speculation.
   - Directly maps to why our system enforces citation-to-evidence-ID
     in generated reports.

## Chain of Custody

A documented, unbroken trail for every evidence item: who collected it,
when, how it was stored, who accessed it, and when it was transferred.
If this chain has a gap or an unauthorized access point, the evidence
can be challenged or excluded in court — regardless of whether its
content is accurate. This is why our system's evidence-schema design
(Week 5) will include source_id, timestamp, and confidence fields: to
preserve a machine-readable version of this chain.

## Why this matters for our project

Our "evidence-aware" RAG system essentially automates the Analysis
phase (correlation + timeline construction) while trying to preserve
the guarantees the Presentation phase requires — every generated
claim must be traceable back to a specific, unaltered piece of
evidence, mirroring how a human investigator's report must cite its
sources.