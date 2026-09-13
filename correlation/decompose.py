import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import json
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def decompose_query(complex_question):
    prompt = f"""You are helping a digital forensics investigator. Break this 
complex question into a sequence of simpler sub-questions that can each be 
answered by retrieving one piece of evidence. Return ONLY valid JSON, no 
markdown, in this format:
{{"sub_queries": ["sub-question 1", "sub-question 2", ...]}}

Complex question: "{complex_question}"
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())

if __name__ == "__main__":
    test_questions = [
        "Who did the suspect communicate with before the incident, and where was that person located at the time?",
        "What happened after John and Mike's call, and did it lead to any data being moved?",
    ]
    
    for q in test_questions:
        print(f"\nComplex question: {q}")
        result = decompose_query(q)
        print("Sub-queries:")
        for i, sq in enumerate(result["sub_queries"], 1):
            print(f"  {i}. {sq}")