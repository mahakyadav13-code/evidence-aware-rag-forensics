import json
from retriever.contradiction_detector import detect_all_contradictions

with open("synthetic_case_v2/evidence.json") as f:
    evidence = json.load(f)

results = detect_all_contradictions(evidence)
total = sum(len(v) for v in results.values())
print(f"Contradictions detected: {total}")
print(json.dumps(results, indent=2))

with open("eval/contradiction_test_results.json", "w") as f:
    json.dump({"total_flags": total, "details": results}, f, indent=2)