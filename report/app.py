import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import json
from generator.report_gen import generate_report
from generator.citation_check import extract_citations, get_valid_evidence_ids
from correlation.timeline import build_timeline

st.set_page_config(page_title="Evidence-Aware RAG for Cybercrime Investigation", layout="wide", page_icon="🕵️")

# ---- Custom styling ----
st.markdown("""
<style>
.main-header {font-size: 2.2rem; font-weight: 700; color: #1a2b4c; margin-bottom: 0;}
.sub-header {color: #6b7280; font-size: 1.05rem; margin-top: 0;}
.metric-box {background: #F2F5FA; padding: 1rem; border-radius: 10px; border: 1px solid #B9C2D0;}
.evid-badge {background: #E8EEF9; color: #1a2b4c; padding: 2px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; margin-right: 4px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🕵️ Evidence-Aware Investigation Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload case evidence and generate a cited, traceable investigator report.</p>', unsafe_allow_html=True)
st.divider()

# ---- Sidebar: Case Data ----
st.sidebar.header("📁 Case Data")
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
            st.sidebar.success(f"✅ Using: {uploaded_file.name}")
    except json.JSONDecodeError:
        st.sidebar.error("Uploaded file is not valid JSON. Using default case instead.")
        evidence_file = default_path
else:
    st.sidebar.info(f"Using synthetic case:\n`{default_path}`")

# ---- Sidebar: Timeline preview ----
with st.sidebar.expander("🕐 Preview Timeline", expanded=False):
    try:
        timeline = build_timeline(evidence_file)
        if len(timeline) == 0:
            st.write("No evidence items found.")
        for event in timeline:
            st.markdown(f"**{event['time']}** &nbsp; `{event['source_type']}`  \n{event['event']}")
    except Exception as e:
        st.error(f"Could not load timeline: {e}")

st.sidebar.divider()
run_clicked = st.sidebar.button("▶️ Run Pipeline: Generate Report", type="primary", use_container_width=True)

# ---- Main area ----
if run_clicked:
    try:
        with st.spinner("Retrieving evidence, correlating, and generating report..."):
            report = generate_report(evidence_file)
        st.success("Report generated successfully!")

        cited = extract_citations(report)
        valid = get_valid_evidence_ids(evidence_file)
        invalid = cited - valid
        unused = valid - cited

        # Top metric row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Citations Used", len(cited))
        with col2:
            st.metric("Invalid Citations", len(invalid), delta_color="inverse")
        with col3:
            st.metric("Uncited Evidence", len(unused))

        tab1, tab2 = st.tabs(["📄 Report", "🔍 Citation Verification"])
        with tab1:
            st.markdown(report)
        with tab2:
            if invalid:
                st.error(f"⚠️ Invalid citations found: {', '.join(invalid)}")
            else:
                st.success(f"✅ All {len(cited)} citations verified as valid evidence IDs")
            if unused:
                st.warning(f"Evidence not cited in report: {', '.join(unused)}")
            else:
                st.info("All available evidence was referenced in the report.")

    except FileNotFoundError:
        st.error("Evidence file not found. Please check the file path or upload a valid file.")
    except Exception as e:
        st.error(f"Pipeline failed: {e}")
        st.info("This could be due to an API issue (rate limit, connectivity) or malformed evidence data. Please try again.")
else:
    st.info("👈 Click **Run Pipeline** in the sidebar to generate an investigator report.")
    st.markdown("### How it works")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**1. Ingest & Correlate**\n\nEvidence is normalized and linked in a knowledge graph.")
    with c2:
        st.markdown("**2. Evidence-Aware Retrieval**\n\nRanked by relevance, reliability, and corroboration.")
    with c3:
        st.markdown("**3. Cited Generation**\n\nEvery claim traces back to a specific evidence ID.")