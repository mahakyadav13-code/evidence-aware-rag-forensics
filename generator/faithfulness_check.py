import sys, os, json, re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_evidence_by_id(evidence_id, evidence_file):
    with open(evidence_file) as f:
        evidence_list = json.load(f)
    clean_id = evidence_id.strip("[]")
    return next((e for e in evidence_list if e["evidence_id"] == clean_id), None)

def check_faithfulness(claim_sentence, evidence_content):
    prompt = f"""Does the following CLAIM logically follow from the EVIDENCE? 
Answer with only "SUPPORTED" or "NOT SUPPORTED" followed by a one-sentence reason.

EVIDENCE: {evidence_content}
CLAIM: {claim_sentence}
"""
    response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
    return response.text.strip()

if __name__ == "__main__":
    # Manually testing a few claim-evidence pairs from the generated report
    test_pairs = [
        ("John placed a phone call to Mike that lasted 14 minutes", "EVID-0001"),
        ("Mike's presence near the old warehouse correlates with his earlier message instructing John to meet him there", "EVID-0005"),
        ("It is unconfirmed which device or individual is associated with IP address 192.168.1.5", "EVID-0003"),
    ]
    
    for claim, eid in test_pairs:
        evidence = get_evidence_by_id(f"[{eid}]", "synthetic_case_v0/evidence.json")
        result = check_faithfulness(claim, evidence["content"])
        print(f"Claim: {claim}")
        print(f"Evidence [{eid}]: {evidence['content']}")
        print(f"Result: {result}\n")