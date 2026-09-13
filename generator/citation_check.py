import sys, os, re, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def extract_citations(report_text):
    return set(re.findall(r'\[EVID-\d+\]', report_text))

def get_valid_evidence_ids(evidence_file):
    with open(evidence_file) as f:
        evidence_list = json.load(f)
    return {f"[{e['evidence_id']}]" for e in evidence_list}

def check_citations(report_file, evidence_file):
    with open(report_file) as f:
        report_text = f.read()
    
    cited = extract_citations(report_text)
    valid = get_valid_evidence_ids(evidence_file)
    
    invalid = cited - valid
    unused = valid - cited
    
    print(f"Citations found in report: {sorted(cited)}")
    print(f"Valid evidence IDs: {sorted(valid)}")
    
    if invalid:
        print(f"\nFAIL: Invalid/hallucinated citations found: {invalid}")
    else:
        print("\nPASS: All citations are valid evidence IDs.")
    
    if unused:
        print(f"Note: Evidence not cited in report: {unused}")

if __name__ == "__main__":
    check_citations("generator/sample_report_v1.md", "synthetic_case_v0/evidence.json")
    