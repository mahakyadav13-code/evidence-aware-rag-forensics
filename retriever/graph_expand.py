import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from kg.kg_builder_from_extraction import build_kg

def expand_via_graph(matched_entity_names, graph, hops=1):
 
    """Given entities matched by initial retrieval, find their graph neighbours."""
    expanded = set(matched_entity_names)
    frontier = set(matched_entity_names)
    
    for _ in range(hops):
        next_frontier = set()
        for node in frontier:
            if node in graph:
                neighbors = set(graph.successors(node)) | set(graph.predecessors(node))
                next_frontier |= neighbors
        expanded |= next_frontier
        frontier = next_frontier
    
    return expanded

def get_evidence_for_entities(entity_names, evidence_file):
    with open(evidence_file) as f:
        evidence_list = json.load(f)
    
    matched_evidence = []
    for item in evidence_list:
        item_entities = set(e.replace("PERSON-", "").replace("DEVICE-", "").replace("IP-", "") 
                            for e in item.get("entity_refs", []))
        if item_entities & entity_names:
            matched_evidence.append(item)
    return matched_evidence

if __name__ == "__main__":
    G = build_kg("ingestion/extracted_entities.json")
    
    # Simulate: initial retrieval matched "Mike"
    initial_match = {"Mike"}
    expanded_entities = expand_via_graph(initial_match, G, hops=1)
    
    print(f"Starting entity: {initial_match}")
    print(f"Expanded (1-hop neighbors): {expanded_entities}\n")
    
    related_evidence = get_evidence_for_entities(expanded_entities, "synthetic_case_v0/evidence.json")
    print(f"Evidence involving expanded entity set:")
    for item in related_evidence:
        print(f"  {item['evidence_id']}: {item['content']}")