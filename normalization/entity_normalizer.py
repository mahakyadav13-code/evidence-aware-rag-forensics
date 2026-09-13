import json

# Simple mapping — real system mein ye fuzzy matching se automate hoga (Week 8)
ENTITY_ALIAS_MAP = {
    "john": "PERSON-John",
    "j. smith": "PERSON-John",
    "mike": "PERSON-Mike",
    "michael": "PERSON-Mike",
}

def normalize_entity(raw_name):
    key = raw_name.strip().lower()
    return ENTITY_ALIAS_MAP.get(key, f"PERSON-{raw_name.strip()}")

def normalize_evidence_entities(evidence_list):
    for item in evidence_list:
        normalized_refs = []
        for ref in item["entity_refs"]:
            normalized_refs.append(ref)
        item["entity_refs"] = normalized_refs
    return evidence_list

if __name__ == "__main__":
    test_names = ["John", "j. smith", "Mike", "Michael"]
    for name in test_names:
        print(f"{name} -> {normalize_entity(name)}")