import csv
import json

def parse_call_logs(filepath):
    evidence_items = []
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            evidence_items.append({
                "evidence_id": f"EVID-CALL-{i:04d}",
                "source_type": "call_log",
                "timestamp": row["timestamp"].replace(" ", "T"),
                "entity_refs": [f"PERSON-{row['caller']}", f"PERSON-{row['receiver']}"],
                "content": f"{row['caller']} called {row['receiver']}. Call lasted {row['duration_min']} minutes.",
                "confidence": 0.95,
                "raw_source_file": filepath
            })
    return evidence_items

if __name__ == "__main__":
    result = parse_call_logs("synthetic_case_v0/raw/call_logs.csv")
    print(json.dumps(result, indent=2))