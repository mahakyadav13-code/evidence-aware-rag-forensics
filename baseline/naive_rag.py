import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from retriever.base import build_vector_store, query_evidence
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def naive_generate_report(evidence_file, query="Summarize the case"):
    """Naive baseline: plain dense retrieval only, no scoring/graph, 
    top-3 results fed directly into generation."""
    collection, model = build_vector_store(evidence_file)
    results = query_evidence(collection, model, query, top_k=3)
    
    context = "\n".join([
        f"[{eid}] {doc}" for eid, doc in zip(results['ids'][0], results['documents'][0])
    ])
    
    prompt = f"""Based on this evidence, write a brief investigator summary. 
Cite evidence IDs in brackets.

EVIDENCE:
{context}

Write the summary now."""
    
    response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
    return response.text

if __name__ == "__main__":
    report = naive_generate_report("synthetic_case_v0/evidence.json")
    print("=== NAIVE BASELINE REPORT ===\n")
    print(report)
    
    with open("baseline/naive_report_v0.md", "w") as f:
        f.write(report)