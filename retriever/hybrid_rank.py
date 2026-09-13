import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from retriever.base import build_vector_store, query_evidence
from retriever.scoring import combined_score
from retriever.graph_expand import expand_via_graph, get_evidence_for_entities
from kg.kg_builder_from_extraction import build_kg

def hybrid_retrieve(query_text, evidence_file, reference_time, 
                     weights=(0.4, 0.3, 0.3)):
    """
    weights: (similarity_weight, evidence_score_weight, graph_bonus_weight)
    """
    w_sim, w_score, w_graph = weights
    
    with open(evidence_file) as f:
        all_evidence = json.load(f)
    
    # Step 1: dense retrieval
    collection, model = build_vector_store(evidence_file)
    dense_results = query_evidence(collection, model, query_text, top_k=len(all_evidence))
    
    # Normalize similarity: convert distance to similarity score (lower distance = higher sim)
    max_dist = max(dense_results['distances'][0]) or 1
    sim_scores = {
        eid: 1 - (dist / max_dist) 
        for eid, dist in zip(dense_results['ids'][0], dense_results['distances'][0])
    }
    
    # Step 2: graph expansion bonus (does this evidence touch a graph-expanded entity?)
    G = build_kg("ingestion/extracted_entities.json")
    # naive: expand from top-1 dense result's entities
    top_evidence = next(e for e in all_evidence if e["evidence_id"] == dense_results['ids'][0][0])
    seed_entities = set(e.replace("PERSON-", "") for e in top_evidence["entity_refs"])
    expanded = expand_via_graph(seed_entities, G, hops=1)
    graph_evidence_ids = {e["evidence_id"] for e in get_evidence_for_entities(expanded, evidence_file)}
    
    # Step 3: combine
    final_scores = []
    for item in all_evidence:
        eid = item["evidence_id"]
        sim = sim_scores.get(eid, 0)
        score = combined_score(item, all_evidence, reference_time)
        graph_bonus = 1.0 if eid in graph_evidence_ids else 0.0
        final = (w_sim * sim) + (w_score * score) + (w_graph * graph_bonus)
        final_scores.append((eid, item["content"], final))
    
    final_scores.sort(key=lambda x: x[2], reverse=True)
    return final_scores

if __name__ == "__main__":
    results = hybrid_retrieve(
        "Who went to the warehouse?", 
        "synthetic_case_v0/evidence.json",
        reference_time="2026-03-05T23:15:00"
    )
    print("Hybrid ranked results:\n")
    for eid, content, score in results:
        print(f"{score:.3f} | {eid}: {content}")