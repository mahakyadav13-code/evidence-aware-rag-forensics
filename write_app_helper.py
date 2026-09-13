content = '''import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import json
from generator.report_gen import generate_report
from generator.citation_check import extract_citations, get_valid_evidence_ids
from correlation.timeline import build_timeline

st.set_page_config(page_title="Evidence-Aware RAG for Cybercrime Investigation", layout="wide")

st.title("Evidence-Aware Investigation Assistant")
st.markdown("Upload case evidence and generate a cited investigator report.")

st.sidebar.header("Case Data")

default_path = "synthetic_case_v0/evidence.json"
uploaded_file = st.sidebar.file_uploader("Upload evidence JSON (or use default)", type="json")

if uploaded_file:
    evidence_data = json.load(uploaded_file)
    evidence_file = "temp_uploaded_evidence.json"
    with open(evidence_file, "w") as f:
        json.dump(evidence_data, f)
    st.sidebar.success("Using uploaded file: " + uploaded_file.name)
else:
    evidence_file = default_path
    st.sidebar.info("Using synthetic case: " + default_path)

with st.sidebar.expander("Preview Timeline"):
    timeline = build_timeline(evidence_file)
    for event in timeline:
        line = "**" + event["time"] + "** [" + event["source_type"] + "] " + event["event"]
        st.write(line)

if st.button("Run Pipeline: Generate Report", type="primary"):
    with st.spinner("Generating investigator report..."):
        report = generate_report(evidence_file)
    st.success("Report generated successfully!")
    tab1, tab2 = st.tabs(["Report", "Citation Verification"])
    with tab1:
        st.markdown(report)
    with tab2:
        cited = extract_citations(report)
        valid = get_valid_evidence_ids(evidence_file)
        invalid = cited - valid
        unused = valid - cited
        if invalid:
            st.error("Invalid citations found: " + str(invalid))
        else:
            st.success("All " + str(len(cited)) + " citations verified as valid evidence IDs")
        if unused:
            st.warning("Evidence not cited in report: " + str(unused))
else:
    st.info("Click the button above to run the full pipeline.")
'''

with open("report/app.py", "w") as f:
    f.write(content)

print("app.py written successfully")