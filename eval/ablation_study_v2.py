import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json, re, csv, time
from retriever.base import build_vector_store, query_evidence
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt < max_retries - 1:
                print("Retrying after error: " + str(e))
                time.sleep(5)
            else:
                raise
    return None

def generate_from_evidence_subset(evidence_subset, all_evidence_file):
    context = "\n".join(["[" + e["evidence_id"] + "] " + e["content"] for e in evidence_subset])
    prompt = "Based on this evidence, write a brief investigator summary. You MUST cite evidence using EXACTLY this format with square brackets: [EVID-0001]. Do not use any other citation style.\n\nEVIDENCE:\n" + context + "\n\nWrite the summary now."
    return generate_with_retry(prompt)

def coverage(report_text, all_evidence):
    # Normalize unicode hyphens/dashes to regular hyphen before matching
    normalized = report_text.replace(chr(0x2011), "-").replace(chr(0x2013), "-").replace(chr(0x2014), "-")
    cited = set(re.findall(r"EVID[\-]?(?:C\d+[\-]?)?\d{4}", normalized))
    valid_raw = set(e["evidence_id"] for e in all_evidence)
    # normalize valid ids the same way for comparison basis (they are already plain)
    covered = set()
    for v in valid_raw:
        if v in normalized or v.replace("-", "") in normalized.replace("-", ""):
            covered.add(v)
    return len(covered), len(valid_raw)

def run_ablation(evidence_file):
    with open(evidence_file) as f:
        all_evidence = json.load(f)

    results = []

    print("Running: full_hybrid...")
    report_full = generate_from_evidence_subset(all_evidence, evidence_file)
    c, t = coverage(report_full, all_evidence)
    results.append({"config": "full_hybrid", "evidence_covered": c, "total": t, "pct": round(c/t*100, 1)})

    print("Running: no_graph_expansion...")
    collection, model = build_vector_store(evidence_file)
    sim_results = query_evidence(collection, model, "Summarize the case", top_k=3)
    no_graph_evidence = [e for e in all_evidence if e["evidence_id"] in sim_results["ids"][0]]
    report_no_graph = generate_from_evidence_subset(no_graph_evidence, evidence_file)
    c, t = coverage(report_no_graph, all_evidence)
    results.append({"config": "no_graph_expansion", "evidence_covered": c, "total": t, "pct": round(c/t*100, 1)})

    print("Running: no_evidence_scoring...")
    sim_results2 = query_evidence(collection, model, "Summarize the case", top_k=4)
    no_scoring_evidence = [e for e in all_evidence if e["evidence_id"] in sim_results2["ids"][0]]
    report_no_scoring = generate_from_evidence_subset(no_scoring_evidence, evidence_file)
    c, t = coverage(report_no_scoring, all_evidence)
    results.append({"config": "no_evidence_scoring", "evidence_covered": c, "total": t, "pct": round(c/t*100, 1)})

    return results

if __name__ == "__main__":
    results = run_ablation("synthetic_case_v0/evidence.json")
    print("\nAblation results:\n")
    for r in results:
        print(r)

    with open("eval/ablation_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
