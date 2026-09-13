from datetime import datetime

def recency_score(timestamp_str, reference_time_str):
    """More recent evidence relative to reference incident time scores higher."""
    ts = datetime.fromisoformat(timestamp_str)
    ref = datetime.fromisoformat(reference_time_str)
    diff_minutes = abs((ref - ts).total_seconds() / 60)
    # Decay: closer in time = higher score, normalize to 0-1
    return max(0, 1 - (diff_minutes / 60))  # within 1 hour window

def reliability_score(confidence):
    """Directly uses the confidence field from evidence schema."""
    return confidence

def corroboration_score(evidence_item, all_evidence):
    """Higher if entities in this evidence also appear in other evidence."""
    this_entities = set(evidence_item.get("entity_refs", []))
    count = 0
    for other in all_evidence:
        if other["evidence_id"] == evidence_item["evidence_id"]:
            continue
        other_entities = set(other.get("entity_refs", []))
        if this_entities & other_entities:  # shared entities
            count += 1
    return min(1.0, count / 3)  # normalize, cap at 1.0

def combined_score(evidence_item, all_evidence, reference_time, 
                    weights=(0.3, 0.4, 0.3)):
    w_recency, w_reliability, w_corroboration = weights
    r = recency_score(evidence_item["timestamp"], reference_time)
    rel = reliability_score(evidence_item["confidence"])
    corr = corroboration_score(evidence_item, all_evidence)
    return (w_recency * r) + (w_reliability * rel) + (w_corroboration * corr)

if __name__ == "__main__":
    import json
    with open("synthetic_case_v0/evidence.json") as f:
        evidence_list = json.load(f)
    
    reference_time = "2026-03-05T23:15:00"  # incident time
    
    print("Evidence scored (recency + reliability + corroboration):\n")
    scored = []
    for item in evidence_list:
        score = combined_score(item, evidence_list, reference_time)
        scored.append((item["evidence_id"], item["content"], score))
    
    scored.sort(key=lambda x: x[2], reverse=True)
    for eid, content, score in scored:
        print(f"{score:.3f} | {eid}: {content}")