import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator.report_gen import generate_report
from generator.citation_check import check_citations

def run_full_pipeline(evidence_file):
    print("="*60)
    print("STEP 1: Generating investigator report")
    print("="*60)
    report = generate_report(evidence_file)
    
    report_path = "generator/final_sample_report.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"\nReport saved to {report_path}\n")
    print(report)
    
    print("\n" + "="*60)
    print("STEP 2: Verifying citation traceability")
    print("="*60)
    check_citations(report_path, evidence_file)

if __name__ == "__main__":
    run_full_pipeline("synthetic_case_v0/evidence.json")