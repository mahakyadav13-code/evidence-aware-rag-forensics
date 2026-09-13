import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from correlation.timeline import build_timeline

REPORT_PROMPT_TEMPLATE = """You are a digital forensics assistant helping an 
investigator understand a case. Below is a chronological timeline of evidence 
from a cybercrime investigation.

TIMELINE:
{timeline_text}

Write a concise investigator report summarizing what happened. CRITICAL RULES:
1. Every factual claim MUST cite the evidence_id in square brackets, e.g. [EVID-0001]
2. Do NOT state anything not directly supported by the evidence below
3. If something is unclear or unconfirmed, say so explicitly rather than guessing
4. End with a "Key findings" section listing the most important connections

Write the report now."""

def build_report_prompt(evidence_file):
    timeline = build_timeline(evidence_file)
    timeline_lines = [
        f"[{e['evidence_id']}] {e['date']} {e['time']} - {e['event']}" 
        for e in timeline
    ]
    timeline_text = "\n".join(timeline_lines)
    return REPORT_PROMPT_TEMPLATE.format(timeline_text=timeline_text)

if __name__ == "__main__":
    prompt = build_report_prompt("synthetic_case_v0/evidence.json")
    print(prompt)