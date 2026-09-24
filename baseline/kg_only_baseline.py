import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from kg.kg_builder_from_extraction import build_kg
from retriever.graph_expand import expand_via_graph, get_evidence_for_entities

def kg_only_retrieve(seed_entity, evidence_file, extraction_file, hops=1):
    G = build_kg(extraction_file)
    expanded = expand_via_graph({seed_entity}, G, hops=hops)
    return get_evidence_for_entities(expanded, evidence_file)

if __name__ == "__main__":
    results = kg_only_retrieve("John", "synthetic_case_v0/evidence.json", "ingestion/extracted_entities.json")
    with open("synthetic_case_v0/evidence.json") as f:
        total = len(json.load(f))
    coverage = len(results) / total * 100
    print(f"KG-only baseline coverage: {coverage:.1f}% ({len(results)}/{total})")
    with open("eval/kg_only_results.json", "w") as f:
        json.dump({"coverage_pct": coverage, "covered": len(results), "total": total}, f, indent=2)