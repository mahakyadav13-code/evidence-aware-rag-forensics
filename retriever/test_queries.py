import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retriever.hybrid_rank import hybrid_retrieve

test_queries = [
    "Who went to the warehouse?",
    "What file did John create?",
    "Did John and Mike communicate?",
    "What happened after the call?",
    "Who uploaded data to an external server?",
]

reference_time = "2026-03-05T23:15:00"

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print('='*60)
    results = hybrid_retrieve(query, "synthetic_case_v0/evidence.json", reference_time)
    for eid, content, score in results[:3]:  # top 3 only
        print(f"{score:.3f} | {eid}: {content}")