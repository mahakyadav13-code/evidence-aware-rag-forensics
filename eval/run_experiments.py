import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json, csv, re
from generator.report_gen import generate_report
from baseline.naive_rag import naive_generate_report

def count_evidence_coverage(report_text, evidence_file):
    with open(evidence_file) as f:
        all_evidence = json.load(f)
    total = len(all_evidence)
    cited = set(re.findall(r'\[([A-Z0-9\-]+)\]', report_text))
    valid_ids = {e["evidence_id"] for e in all_evidence}
    covered = cited & valid_ids
    return len(covered), total, len(covered) / total if total > 0 else 0

def run_experiment(evidence_file, case_name):
    results = []
    
    # Hybrid system (our full pipeline)
    hybrid_report = generate_report(evidence_file)
    h_covered, h_total, h_coverage = count_evidence_coverage(hybrid_report, evidence_file)
    results.append({
        "case": case_name, "system": "hybrid",
        "evidence_covered": h_covered, "total_evidence": h_total,
        "coverage_pct": round(h_coverage * 100, 1)
    })
    
    # Naive baseline
    naive_report = naive_generate_report(evidence_file)
    n_covered, n_total, n_coverage = count_evidence_coverage(naive_report, evidence_file)
    results.append({
        "case": case_name, "system": "naive_baseline",
        "evidence_covered": n_covered, "total_evidence": n_total,
        "coverage_pct": round(n_coverage * 100, 1)
    })
    
    return results

if __name__ == "__main__":
    all_results = []
    all_results += run_experiment("synthetic_case_v0/evidence.json", "case_v0")
    all_results += run_experiment("synthetic_case_v1/evidence.json", "case_v1")
    
    print("Results:\n")
    for r in all_results:
        print(r)
    
    with open("eval/results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)