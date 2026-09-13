import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from retriever.hybrid_rank import hybrid_retrieve

def load_evidence(evidence_file):
    with open(evidence_file) as f:
        return json.load(f)

def get_timestamp_after(evidence_item):
    return evidence_item["timestamp"]

def iterative_multihop(evidence_file, reference_time):
    """
    Step 1: find the call event
    Step 2: use its timestamp to filter subsequent evidence
    Step 3: retrieve semantically relevant evidence AFTER that timestamp
    """
    all_evidence = load_evidence(evidence_file)
    
    # Step 1: retrieve the call
    step1_results = hybrid_retrieve("call between John and Mike", evidence_file, reference_time)
    call_evidence = step1_results[0]
    call_timestamp = next(e["timestamp"] for e in all_evidence if e["evidence_id"] == call_evidence[0])
    print(f"Step 1 - Found call: {call_evidence[1]} at {call_timestamp}")
    
    # Step 2: filter evidence to only those AFTER the call timestamp
    later_evidence = [e for e in all_evidence if e["timestamp"] > call_timestamp]
    print(f"\nStep 2 - Evidence after call timestamp ({len(later_evidence)} items):")
    for e in later_evidence:
        print(f"  {e['evidence_id']} ({e['timestamp']}): {e['content']}")
    
    # Step 3: within that filtered set, do semantic search for "data moved"
    later_ids = {e["evidence_id"] for e in later_evidence}
    step3_results = hybrid_retrieve("data transfer or file movement", evidence_file, reference_time)
    filtered_step3 = [r for r in step3_results if r[0] in later_ids]
    
    print(f"\nStep 3 - Most relevant among later evidence:")
    for eid, content, score in filtered_step3[:2]:
        print(f"  {score:.3f} | {eid}: {content}")

if __name__ == "__main__":
    iterative_multihop("synthetic_case_v0/evidence.json", "2026-03-05T23:15:00")