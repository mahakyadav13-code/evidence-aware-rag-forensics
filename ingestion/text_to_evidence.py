import os, json, re
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

EXTRACTION_PROMPT = """You are converting a free-text case description into structured 
digital evidence items. Extract each distinct fact/event as one evidence item.

For each item, output a JSON object with these exact fields:
- evidence_id: sequential, e.g. "EVID-0001"
- source_type: one of ["chat_log", "call_log", "file_metadata", "network_log", "location_ping"]
- timestamp: ISO 8601 format (e.g. "2026-03-05T22:30:00"). If no date is given, use "2026-01-01" as the date and infer time from context, or "2026-01-01T00:00:00" if unknown.
- entity_refs: list of normalized entity IDs, e.g. ["PERSON-John", "DEVICE-JohnLaptop"]
- content: the plain-text description of this fact
- confidence: a number 0-1 estimating how reliable this fact seems from the text
- raw_source_file: "user_input"

Return ONLY a valid JSON array, no explanation, no markdown formatting.

CASE TEXT:
{case_text}
"""

def convert_text_to_evidence(case_text: str) -> list:
    prompt = EXTRACTION_PROMPT.format(case_text=case_text)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    raw = response.text.strip()
    raw = re.sub(r"^```json|```$", "", raw, flags=re.MULTILINE).strip()
    try:
        evidence = json.loads(raw)
        if not isinstance(evidence, list):
            raise ValueError("Expected a JSON list")
        return evidence
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse LLM output as JSON: {e}\nRaw output:\n{raw}")