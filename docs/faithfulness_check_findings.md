# Faithfulness Check Findings — Week 11 Day 4

## Result: 1/3 claims marked SUPPORTED by single-evidence checking

## Key limitation discovered
Our faithfulness checker validates each claim against ONE evidence 
item at a time. This produces false negatives for two claim types:

1. **Multi-evidence synthesis claims**: "Mike's location correlates 
   with his message" draws on BOTH EVID-0004 (message) and EVID-0005 
   (location), but checking against EVID-0005 alone correctly finds 
   no mention of the message — the claim isn't wrong, the check is 
   incomplete.

2. **Meta-level uncertainty claims**: "It is unconfirmed whether X" 
   is a valid epistemic statement about the evidence, but literal 
   evidence text never contains the word "unconfirmed" — so a naive 
   support check fails these by design.

## Implication for the system
A production faithfulness checker needs to:
- Check claims against the FULL evidence set (or all cited IDs), 
  not one at a time
- Distinguish between factual claims (should map to evidence text) 
  and uncertainty/epistemic claims (should map to ABSENCE of 
  evidence, which is a different check)

This is a valuable limitation to discuss in the paper's Discussion 
section as future work.