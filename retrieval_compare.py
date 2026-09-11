from rank_bm25 import BM25Okapi
import chromadb

documents = [
    "John called Mike at 10:30 PM on the night of the incident.",
    "The IP address 192.168.1.5 accessed the server at midnight.",
    "A file named 'transfer.zip' was created on the suspect's laptop.",
    "Mike sent a message saying 'meet me at the warehouse'.",
    "The suspect's phone location pinged near the warehouse at 11 PM."
]

query = "Who did the suspect contact around the time of the incident?"

# --- BM25 (sparse/keyword-based) ---
tokenized_docs = [doc.lower().split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)
tokenized_query = query.lower().split()
bm25_scores = bm25.get_scores(tokenized_query)

print("=== BM25 (keyword-based) RESULTS ===")
ranked_bm25 = sorted(zip(documents, bm25_scores), key=lambda x: x[1], reverse=True)
for doc, score in ranked_bm25[:3]:
    print(f"Score: {score:.4f} | {doc}")

# --- Dense retrieval (ChromaDB, semantic) ---
client = chromadb.Client()
collection = client.create_collection("retrieval_compare")
ids = [f"doc{i}" for i in range(len(documents))]
collection.add(documents=documents, ids=ids)

results = collection.query(query_texts=[query], n_results=3)

print("\n=== DENSE (semantic) RESULTS ===")
for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"Score: {dist:.4f} | {doc}")