from dotenv import load_dotenv
import os
import json
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_entities_and_relations(evidence_text):
    prompt = f"""Extract entities and relations from this evidence text. 
Return ONLY valid JSON, no other text, no markdown code blocks, in this exact format:
{{
  "entities": [{{"name": "...", "type": "PERSON|DEVICE|LOCATION|IP|ORG"}}],
  "relations": [{{"subject": "...", "relation": "...", "object": "..."}}]
}}

Evidence text: "{evidence_text}"
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    raw_output = response.text.strip()
    if raw_output.startswith("```"):
        raw_output = raw_output.split("```")[1]
        if raw_output.startswith("json"):
            raw_output = raw_output[4:]
    return json.loads(raw_output.strip())

if __name__ == "__main__":
    with open("synthetic_case_v0/evidence.json") as f:
        evidence_list = json.load(f)
    
    all_extractions = []
    for item in evidence_list:
        result = extract_entities_and_relations(item["content"])
        result["evidence_id"] = item["evidence_id"]
        all_extractions.append(result)
        print(f"\n{item['evidence_id']}: {item['content']}")
        print(json.dumps(result, indent=2))
    
    with open("ingestion/extracted_entities.json", "w") as f:
        json.dump(all_extractions, f, indent=2)