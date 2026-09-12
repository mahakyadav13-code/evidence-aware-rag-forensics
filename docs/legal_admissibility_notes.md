# Legal & Admissibility Considerations — Week 4 Day 4

## Why this matters technically
Digital evidence is only useful in an investigation/court if its 
origin, integrity, and chain of custody can be proven. An AI system 
that generates conclusions without traceable sourcing produces 
output that is legally worthless, no matter how accurate it sounds.

## Key concepts
- Chain of custody: unbroken record of who handled evidence, when, and how
- Section 65B (Indian Evidence Act): electronic evidence requires a 
  certificate establishing authenticity to be admissible in Indian courts
- Provenance: every piece of evidence must be traceable to its exact 
  source file, timestamp, and extraction method

## What "evidence-aware" must technically guarantee
1. Every generated claim must cite the exact evidence ID it came from 
   (no unsupported synthesis)
2. No fabricated links between entities that aren't backed by actual 
   retrieved evidence
3. Full traceability: given any output claim, an investigator must be 
   able to trace back to the raw source

## Relevance to our project
This is the legal justification for our citation/faithfulness-check 
module (Week 11) — it's not just a quality feature, it's what would 
make (or break) real-world admissibility of system-generated findings.