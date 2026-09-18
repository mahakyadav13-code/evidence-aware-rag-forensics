from datetime import datetime

def compute_corroboration_count(item, all_evidence):
    """Count independent sources (different source_type) sharing an entity with this item."""
    shared_entities = set(item["entity_refs"])
    corroborating_sources = set()
    for other in all_evidence:
        if other["evidence_id"] == item["evidence_id"]:
            continue
        if shared_entities & set(other["entity_refs"]):
            corroborating_sources.add(other["source_type"])
    return len(corroborating_sources)

def compute_temporal_consistency(cited_items):
    """Checks if cited evidence timestamps form a plausible non-conflicting sequence
    (no two items placing the same entity in two different locations at the same time)."""
    location_events = [i for i in cited_items if i["source_type"] == "location_ping"]
    for a in location_events:
        for b in location_events:
            if a["evidence_id"] == b["evidence_id"]:
                continue
            same_entity = set(a["entity_refs"]) & set(b["entity_refs"])
            same_time = a["timestamp"] == b["timestamp"]
            diff_location = a["content"] != b["content"]
            if same_entity and same_time and diff_location:
                return 0.0  # contradiction found
    return 1.0

def compute_confidence(cited_items, all_evidence):
    """
    Combines:
    - avg_reliability: mean of confidence field across cited evidence
    - avg_corroboration: mean number of independent corroborating sources
    - temporal_consistency: 1.0 if no contradictions, 0.0 if found
    Returns a score 0-1 and a human-readable label.
    """
    if not cited_items:
        return {"score": 0.0, "label": "Low", "details": {}}

    avg_reliability = sum(i["confidence"] for i in cited_items) / len(cited_items)

    corroboration_counts = [compute_corroboration_count(i, all_evidence) for i in cited_items]
    avg_corroboration = sum(corroboration_counts) / len(corroboration_counts)
    norm_corroboration = min(avg_corroboration / 3, 1.0)  # cap at 3+ sources = max score

    temporal_score = compute_temporal_consistency(cited_items)

    final_score = (0.4 * avg_reliability) + (0.35 * norm_corroboration) + (0.25 * temporal_score)

    if final_score >= 0.75:
        label = "High"
    elif final_score >= 0.5:
        label = "Medium"
    else:
        label = "Low"

    return {
        "score": round(final_score, 3),
        "label": label,
        "details": {
            "avg_reliability": round(avg_reliability, 3),
            "avg_corroboration": round(avg_corroboration, 2),
            "temporal_consistency": temporal_score
        }
    }