# Baseline vs Hybrid Comparison — Week 13 Day 3

## Naive baseline report (top-3 dense retrieval only)
Covers: call, message, location ping.
MISSES: file creation (EVID-0002) and file upload (EVID-0003) — 
the two most critical pieces of evidence for a data exfiltration case.

## Our hybrid system report (Week 11)
Covers all 5 evidence items, including the file creation/upload chain, 
because evidence scoring (recency+reliability+corroboration) and 
graph-expansion surface evidence that pure top-3 similarity search 
would drop.

## Conclusion
This concretely demonstrates the value of evidence-aware retrieval: 
the naive baseline would produce a report that misses the actual 
crime (data exfiltration), reporting only a fraction of the case.