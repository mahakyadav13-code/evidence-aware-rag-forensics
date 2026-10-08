import time
import sys, os, json, csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator.report_gen import generate_report
from generator.citation_check import extract_citations, get_valid_evidence_ids
from baseline.naive_rag import naive_generate_report

CASES = ["synthetic_case_v0", "synthetic_case_v1", "synthetic_case_v5", "synthetic_case_v6"]

rows = []
for case in CASES:
    ev_file = f"{case}/evidence.json"
    if not os.path.exists(ev_file):
        print(f"Skipping {case}: no evidence.json found")
        continue
    valid = get_valid_evidence_ids(ev_file)
    total = len(valid)

    try:
        hybrid_report = generate_report(ev_file)
        h_cited = extract_citations(hybrid_report) & valid
        rows.append([case, "hybrid", len(h_cited), total, round(len(h_cited)/total*100, 1)])
        print(f"{case} hybrid: {len(h_cited)}/{total}")
    except Exception as e:
        print(f"Hybrid failed on {case}: {e}")

    try:
        naive_report = naive_generate_report(ev_file)
        n_cited = extract_citations(naive_report) & valid
        rows.append([case, "naive_baseline", len(n_cited), total, round(len(n_cited)/total*100, 1)])
        print(f"{case} naive: {len(n_cited)}/{total}")
    except Exception as e:
        print(f"Naive failed on {case}: {e}")

with open("eval/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["case", "system", "evidence_covered", "total_evidence", "coverage_pct"])
    writer.writerows(rows)

print("Done.")