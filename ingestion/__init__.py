import json
from ingestion.call_log_parser import parse_call_logs

def run_test():
    # Test 1: our own parser output matches schema
    parsed = parse_call_logs("synthetic_case_v0/raw/call_logs.csv")
    print("Parsed call log evidence:")
    print(json.dumps(parsed, indent=2))
    
    # Test 2: validate required fields exist
    required_fields = ["evidence_id", "source_type", "timestamp", 
                        "entity_refs", "content", "confidence"]
    for item in parsed:
        missing = [f for f in required_fields if f not in item]
        if missing:
            print(f"FAIL: {item.get('evidence_id')} missing fields: {missing}")
        else:
            print(f"PASS: {item['evidence_id']} has all required fields")
    
    # Test 3: check against contributor's full synthetic case
    with open("synthetic_case_v0/evidence.json") as f:
        full_case = json.load(f)
    print(f"\nFull synthetic case has {len(full_case)} evidence items across types:")
    types = set(item["source_type"] for item in full_case)
    print(types)

if __name__ == "__main__":
    run_test()