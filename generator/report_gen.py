import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from google import genai
from generator.report_prompt import build_report_prompt

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_report(evidence_file):
    prompt = build_report_prompt(evidence_file)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    report = generate_report("synthetic_case_v0/evidence.json")
    print(report)
    
    with open("generator/sample_report_v1.md", "w") as f:
        f.write(report)