import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from correlation.decompose import decompose_query
from retriever.hybrid_rank import hybrid_retrieve

def run_multihop(complex_question, evidence_file, reference_time):
    decomposition = decompose_query(complex_question)
    sub_queries = decomposition["sub_queries"]
    
    print(f"Complex question: {complex_question}\n")
    all_results = {}
    for i, sq in enumerate(sub_queries, 1):
        print(f"Sub-query {i}: {sq}")
        results = hybrid_retrieve(sq, evidence_file, reference_time)
        top_result = results[0]
        print(f"  Top evidence: {top_result[1]} (score: {top_result[2]:.3f})\n")
        all_results[sq] = results[:2]
    
    return all_results

if __name__ == "__main__":
    question = "What happened after John and Mike's call, and did it lead to any data being moved?"
    run_multihop(question, "synthetic_case_v0/evidence.json", "2026-03-05T23:15:00")