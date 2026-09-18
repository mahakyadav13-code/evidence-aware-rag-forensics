import json
from retriever.contradiction_detector import detect_all_contradictions

with open("synthetic_case_v0/evidence.json") as f:
    all_evidence = json.load(f)

results = detect_all_contradictions(all_evidence)
print(json.dumps(results, indent=2))