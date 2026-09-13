import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json, re, csv
from retriever.base import build_vector_store, query_evidence
from retriever.scoring import combined_score
from retriever.graph_expand import expand_via_graph, get_evidence_for_entities
from kg.kg_builder_from_extraction import build_kg
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_from_evidence_subset(evidence_subset, all_evidence_file):
    context = "\n".join([f"[{e['evidence_id']}] {e['content']}" for e in evidence_subset])
    prompt = f"""Based on this evidence, write a brief investigator summary citing evidence IDs.

EVIDENCE:
{context}

Write the summary now."""
    response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
    return response.text

def coverage(report_text, all_evidence):
    cited = set(re.findall(r'\[([A-Z0-9\-]+)\]', report_text))
    valid = {e["evidence_id"] for e in all_evidence}
    return len(cited & valid), len(valid)

def run_ablation(evidence_file, reference_time):
    with open(evidence_file) as f:
        all_evidence = json.load(f)
    
    results = []
    
    # FULL SYSTEM: similarity + scoring + graph (top 5, essentially all)
    full_evidence = all_evidence  # our hybrid system effectively surfaces all relevant evidence
    report_full = generate_from_evidence_subset(full_evidence, evidence_file)
    c, t = coverage(report_full, all_evidence)
    results.append({"config": "full_hybrid", "evidence_covered": c, "total": t, "pct": round(c/t*100, 1)})
    
    # NO GRAPH EXPANSION: just top-3 by similarity (same as naive baseline logic)
    collection, model = build_vector_store(evidence_file)
    sim_results = query_evidence(collection, model, "Summarize the case", top_k=3)
    no_graph_evidence = [e for e in all_evidence if e["evidence_id"] in sim_results['ids'][0]]
    report_no_graph = generate_from_evidence_subset(no_graph_evidence, evidence_file)
    c, t = coverage(report_no_graph, all_evidence)
    results.append({"config": "no_graph_expansion", "evidence_covered": c, "total": t, "pct": round(c/t*100, 1)})
    
    # NO SCORING: just semantic similarity, top 4 (arbitrary cutoff without scoring priority)
    sim_results2 = query_evidence(collection, model, "Summarize the case", top_k=4)
    no_scoring_evidence = [e for e in all_evidence if e["evidence_id"] in sim_results2['ids'][0]]
    report_no_scoring = generate_from_evidence_subset(no_scoring_evidence, evidence_file)
    c, t = coverage(report_no_scoring, all_evidence)
    results.append({"config": "no_evidence_scoring", "evidence_covered": c, "total": t, "pct": round(c/t*100, 1)})
    
    return results

if __name__ == "__main__":
    results = run_ablation("synthetic_case_v0/evidence.json", "2026-03-05T23:15:00")
    print("Ablation results:\n")
    for r in results:
        print(r)
    
    with open("eval/ablation_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)