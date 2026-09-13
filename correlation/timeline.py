import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from datetime import datetime

def build_timeline(evidence_file):
    with open(evidence_file) as f:
        evidence_list = json.load(f)
    
    sorted_evidence = sorted(evidence_list, key=lambda e: e["timestamp"])
    
    timeline = []
    for item in sorted_evidence:
        ts = datetime.fromisoformat(item["timestamp"])
        timeline.append({
            "time": ts.strftime("%H:%M:%S"),
            "date": ts.strftime("%Y-%m-%d"),
            "evidence_id": item["evidence_id"],
            "source_type": item["source_type"],
            "event": item["content"],
            "entities": item["entity_refs"]
        })
    return timeline

def print_timeline(timeline):
    print("CASE TIMELINE\n" + "="*50)
    for event in timeline:
        print(f"{event['date']} {event['time']} | [{event['source_type']}] {event['event']}")

if __name__ == "__main__":
    timeline = build_timeline("synthetic_case_v0/evidence.json")
    print_timeline(timeline)
    
    with open("correlation/case_timeline.json", "w") as f:
        json.dump(timeline, f, indent=2)