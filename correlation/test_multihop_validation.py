import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from correlation.decompose import decompose_query
from correlation.timeline import build_timeline

test_questions = [
    "Who did John communicate with before creating the file?",
    "What happened between the call and the file upload?",
    "Did Mike's location connect to the message he sent?",
]

timeline = build_timeline("synthetic_case_v0/evidence.json")

for q in test_questions:
    print(f"\n{'='*60}")
    print(f"Question: {q}")
    decomposition = decompose_query(q)
    print("Decomposed into:")
    for i, sq in enumerate(decomposition["sub_queries"], 1):
        print(f"  {i}. {sq}")

print(f"\n{'='*60}")
print("Reference timeline for manual comparison:")
for event in timeline:
    print(f"  {event['time']} - {event['event']}")