import json
from retriever.confidence_calc import compute_confidence

with open("synthetic_case_v0/evidence.json") as f:
    all_evidence = json.load(f)

# Simulate citing 3 items (John's call, file, upload)
cited = [e for e in all_evidence if e["evidence_id"] in ["EVID-0001", "EVID-0002", "EVID-0003"]]

result = compute_confidence(cited, all_evidence)
print(json.dumps(result, indent=2))