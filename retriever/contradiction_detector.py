from datetime import datetime

def detect_location_contradictions(all_evidence):
    """Same entity, overlapping time window, different locations."""
    contradictions = []
    location_events = [e for e in all_evidence if e["source_type"] == "location_ping"]

    for i, a in enumerate(location_events):
        for b in location_events[i+1:]:
            shared_entities = set(a["entity_refs"]) & set(b["entity_refs"])
            if not shared_entities:
                continue
            t_a = datetime.fromisoformat(a["timestamp"])
            t_b = datetime.fromisoformat(b["timestamp"])
            diff_minutes = abs((t_a - t_b).total_seconds() / 60)
            if diff_minutes <= 10 and a["content"] != b["content"]:
                contradictions.append({
                    "type": "location_conflict",
                    "entities": list(shared_entities),
                    "evidence_ids": [a["evidence_id"], b["evidence_id"]],
                    "detail": f"{a['content']} vs {b['content']} within {diff_minutes:.0f} min"
                })
    return contradictions

def detect_timeline_contradictions(all_evidence):
    """Same entity appears to perform two mutually exclusive actions at the same timestamp."""
    contradictions = []
    by_time = {}
    for e in all_evidence:
        by_time.setdefault(e["timestamp"], []).append(e)

    for ts, items in by_time.items():
        if len(items) < 2:
            continue
        for i, a in enumerate(items):
            for b in items[i+1:]:
                shared_entities = set(a["entity_refs"]) & set(b["entity_refs"])
                if shared_entities and a["source_type"] != b["source_type"]:
                    # Two different simultaneous actions for the same entity — flag as worth review
                    contradictions.append({
                        "type": "simultaneous_action",
                        "entities": list(shared_entities),
                        "evidence_ids": [a["evidence_id"], b["evidence_id"]],
                        "detail": f"Same timestamp ({ts}): {a['content']} AND {b['content']}"
                    })
    return contradictions

def detect_reliability_conflict(all_evidence, threshold_gap=0.3):
    """Two sources reference the same entity/event but with very different confidence — flag for review."""
    contradictions = []
    for i, a in enumerate(all_evidence):
        for b in all_evidence[i+1:]:
            shared_entities = set(a["entity_refs"]) & set(b["entity_refs"])
            if shared_entities and abs(a["confidence"] - b["confidence"]) >= threshold_gap:
                contradictions.append({
                    "type": "reliability_gap",
                    "entities": list(shared_entities),
                    "evidence_ids": [a["evidence_id"], b["evidence_id"]],
                    "detail": f"Confidence gap: {a['evidence_id']}={a['confidence']} vs {b['evidence_id']}={b['confidence']}"
                })
    return contradictions

def detect_all_contradictions(all_evidence):
    return {
        "location_conflicts": detect_location_contradictions(all_evidence),
        "simultaneous_actions": detect_timeline_contradictions(all_evidence),
        "reliability_gaps": detect_reliability_conflict(all_evidence)
    }