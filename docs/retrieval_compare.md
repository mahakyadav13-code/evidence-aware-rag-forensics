# BM25 vs Dense Retrieval — Day 4

BM25 (keyword-based) ranks documents by exact word overlap with the query. 
It works well when evidence uses the same wording as the question, but 
misses relevant evidence phrased differently (e.g. "pinged near the 
warehouse" vs a query asking about "contact" — no shared keywords).

Dense retrieval (embeddings) captures semantic meaning, so it correctly 
surfaced evidence like the phone-ping and call records even without 
literal keyword matches to "contact."

Decision: for the evidence-aware RAG system, dense retrieval alone isn't 
enough either — cybercrime evidence often has exact identifiers (IPs, 
file names, phone numbers) where keyword matching is more reliable than 
semantic similarity. We will use hybrid retrieval (BM25 + dense combined) 
in the final retriever module.