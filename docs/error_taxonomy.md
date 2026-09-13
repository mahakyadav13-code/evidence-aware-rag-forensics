# Error Taxonomy — Week 14 Day 1

## Category 1: Entity Resolution Failures
**Example:** "warehouse" vs "old warehouse" treated as separate KG 
nodes (Week 8 Day 5), even though they refer to the same location.
**Root cause:** LLM extracts entities per-evidence-item in isolation, 
with no cross-evidence normalization step.
**Impact:** Breaks graph connectivity, could cause the retriever to 
miss a correlation an investigator would catch instantly.

## Category 2: Missing Cross-Evidence Inference
**Example:** IP address 192.168.1.5 was never explicitly linked to 
John in the KG (Week 8 Day 5), even though ground truth implies it's 
his device.
**Root cause:** Relation extraction only captures what's explicitly 
stated in each evidence item's text, not inferences requiring 
combining multiple pieces of evidence.
**Impact:** Underlying case logic (attribution) has to be reconstructed 
manually rather than surfaced automatically.

## Category 3: Temporal Reasoning Gaps
**Example:** Query "What happened after the call?" initially returned 
the call itself as top result (Week 9 Day 5), before being fixed by 
explicit timestamp filtering (Week 10 Day 3).
**Root cause:** Pure semantic similarity has no concept of "before/
after" — temporal keywords in a query don't translate to numeric 
timestamp comparisons without dedicated logic.
**Impact:** Without the Week 10 fix, retrieval for temporally-scoped 
questions would be unreliable.

## Category 4: Faithfulness-Checking Limitations
**Example:** Valid claims synthesizing multiple evidence items, or 
expressing appropriate uncertainty ("it is unconfirmed whether..."), 
were incorrectly flagged NOT SUPPORTED when checked against a single 
evidence item (Week 11 Day 4).
**Root cause:** Our faithfulness checker compares one claim to one 
evidence item; it has no mechanism for multi-evidence synthesis or 
distinguishing factual vs epistemic claim types.
**Impact:** A naive faithfulness gate would incorrectly reject good, 
well-hedged report content.

## Summary
3 of 4 error categories stem from the same underlying limitation: 
the system processes evidence item-by-item rather than holistically. 
This is a natural direction for future work — see Discussion section.