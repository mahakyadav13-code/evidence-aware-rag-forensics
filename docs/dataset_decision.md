# Dataset Decision — Week 5 Day 3

## Public options reviewed
- NIST CFReDS Portal, DFRWS Challenges, Digital Corpora, Enron Emails

## Decision
Public forensic datasets are raw disk/memory images requiring separate 
extraction tooling, and mostly lack complete ground-truth relationship 
data needed to evaluate correlation accuracy. We will build a small 
**synthetic case dataset** instead: a fictional cybercrime case with 
3-5 evidence sources (chat log, call log, file metadata, network log) 
and a known ground-truth timeline/relationship map, modeled after the 
real DFRWS 2011 case structure reviewed in Week 4. This gives us full 
control over ground truth for evaluation while still reflecting a 
realistic multi-source scenario.

(Optional future extension: incorporate Enron email data as a 
supplementary real-text source once the core pipeline works.)