# Data Design Doc v1 — Week 5 Day 6

## Summary
We finalized a synthetic case dataset (`synthetic_case_v0/`) modeling a 
fictional cybercrime scenario with 5 evidence items across 5 evidence 
types (call log, chat log, file metadata, network log, location ping), 
each conforming to our common evidence schema (Week 5 Day 4).

## Validation performed
- Confirmed all evidence entries include every required schema field
- Confirmed entity IDs are consistent across all sources (e.g. 
  "PERSON-John" used identically in call, chat, file, and network 
  evidence — required for knowledge-graph construction in Week 8)
- Verified timestamps align correctly with the ground-truth timeline

## Status
Dataset v0 is ready to be used as the primary test case for Phase 3 
(architecture design) and Phase 4 (implementation). We will expand this 
to 3-5 total cases in Week 13 for proper evaluation.

## Next step
Proceed to Phase 3 (Week 6): full system architecture design.