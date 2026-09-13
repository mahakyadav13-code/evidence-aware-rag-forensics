# NER Approach Decision

## Options considered

**spaCy NER (Week 3 experiment)**
- Pros: Fast, free, no API calls, good for standard entities (PERSON, DATE, TIME, ORG)
- Cons: Cannot extract relations between entities; misses domain-specific 
  entities (e.g. IP addresses, device IDs, evidence-specific terms)

**LLM-based extraction (Claude API)**
- Pros: Can extract both entities AND relations in one pass; understands 
  context (e.g. "the suspect" refers to a previously named person); 
  flexible to domain-specific entity types
- Cons: API cost per call; slower than spaCy; needs careful prompt design 
  to avoid hallucinated entities/relations

## Decision
Use LLM-based extraction (Claude API) for our system, since our evidence-aware 
RAG needs both entities AND relations (Week 3 Day 3 showed spaCy alone can't 
extract relations — they had to be manually defined). 

Design principle: prompt the LLM to extract entities and relations as 
structured JSON, so output is directly usable for KG construction (Day 4).