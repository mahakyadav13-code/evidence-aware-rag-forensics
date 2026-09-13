# Retriever Test Notes — Week 9 Day 5

## Queries tested: 5
4/5 returned intuitively correct top results.

## Limitation found
Query "What happened after the call?" returned the call itself as 
the top result, rather than events chronologically after it. This 
shows the current retriever handles semantic similarity well but 
has no temporal/sequential reasoning — it cannot interpret "after X" 
as a chronological filter. This is the gap Week 10 (timeline builder, 
multi-hop query decomposition) is designed to address.