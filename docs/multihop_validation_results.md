# Multi-Hop Validation Results — Week 10 Day 5

## Question 1: Who did John communicate with before creating the file?
Decomposition correctly sequences: file timestamp → prior 
communications → sender/recipient identification. Matches ground 
truth: John called Mike (22:30) before file creation (22:52).

## Question 2: What happened between the call and file upload?
Decomposition is thorough (5 sub-queries covering process logs, 
file access, network traffic) but slightly over-engineered for 
our synthetic case — we don't have process execution or browsing 
history evidence types. Shows the decomposition logic generalizes 
well beyond our current schema, which is good for future scale.

## Question 3: Did Mike's location connect to the message he sent?
Strong decomposition — separately asks about (a) location mentioned 
IN the message text vs (b) actual GPS location at send time. This 
maps directly to our Week 8 finding: "warehouse" (message content) 
vs "old warehouse" (GPS ping) are technically different evidence 
types that need correlation, not automatic assumption of identity.

## Conclusion
Query decomposition (Week 10 Day 1-3) combined with timeline 
building (Day 4) successfully supports multi-hop investigator 
reasoning. Remaining gap: entity resolution for near-duplicate 
location references (see Week 8 Day 5 sanity check).