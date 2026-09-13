from sentence_transformers import SentenceTransformer
import chromadb
import json

def build_vector_store(evidence_file, collection_name="case_evidence"):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    with open(evidence_file) as f:
        evidence_list = json.load(f)
    
    client = chromadb.Client()
    collection = client.create_collection(collection_name)
    
    contents = [item["content"] for item in evidence_list]
    embeddings = model.encode(contents).tolist()
    ids = [item["evidence_id"] for item in evidence_list]
    metadatas = [{"source_type": item["source_type"], 
                  "timestamp": item["timestamp"],
                  "confidence": item["confidence"]} for item in evidence_list]
    
    collection.add(
        embeddings=embeddings,
        documents=contents,
        ids=ids,
        metadatas=metadatas
    )
    
    return collection, model

def query_evidence(collection, model, query_text, top_k=3):
    query_embedding = model.encode([query_text]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    return results

if __name__ == "__main__":
    collection, model = build_vector_store("synthetic_case_v0/evidence.json")
    
    test_query = "Who went to the warehouse?"
    results = query_evidence(collection, model, test_query)
    
    print(f"Query: {test_query}\n")
    for i, (doc, meta, dist) in enumerate(zip(
        results['documents'][0], 
        results['metadatas'][0], 
        results['distances'][0]
    )):
        print(f"{i+1}. [{meta['source_type']}] {doc} (distance: {dist:.3f})")
        