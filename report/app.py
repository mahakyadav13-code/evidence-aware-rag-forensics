import sys, os
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

evidence_file = default_path
if uploaded_file:
    try:
        evidence_data = json.load(uploaded_file)
        if not isinstance(evidence_data, list) or len(evidence_data) == 0:
            st.sidebar.error("Uploaded file must be a non-empty JSON list of evidence items.")
        else:
            evidence_file = "temp_uploaded_evidence.json"
            with open(evidence_file, "w") as f:
                json.dump(evidence_data, f)
            st.sidebar.success("Using uploaded file: " + uploaded_file.name)
    except json.JSONDecodeError:
        st.sidebar.error("Uploaded file is not valid JSON. Using default case instead.")
        evidence_file = default_path
else:
    st.sidebar.info("Using synthetic case: " + default_path)

with st.sidebar.expander("Preview Timeline"):
    try:
        timeline = build_timeline(evidence_file)
        if len(timeline) == 0:
            st.write("No evidence items found.")
        for event in timeline:
            line = "**" + event["time"] + "** [" + event["source_type"] + "] " + event["event"]
            st.write(line)
    except Exception as e:
        st.error("Could not load timeline: " + str(e))

if st.button("Run Pipeline: Generate Report", type="primary"):
    try:
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
    except FileNotFoundError:
        st.error("Evidence file not found. Please check the file path or upload a valid file.")
    except Exception as e:
        st.error("Pipeline failed: " + str(e))
        st.info("This could be due to an API issue (rate limit, connectivity) or malformed evidence data. Please try again.")
else:
    st.info("Click the button above to run the full pipeline.")
