import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import json
from generator.report_gen import generate_report
from generator.citation_check import extract_citations, get_valid_evidence_ids
from correlation.timeline import build_timeline

st.set_page_config(page_title="Evidence-Aware RAG for Cybercrime Investigation", layout="wide", page_icon="🔎")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero {
    background: linear-gradient(135deg, #1a2b4c 0%, #2E4A7A 60%, #B4650A 130%);
    padding: 2.2rem 2.5rem; border-radius: 16px; margin-bottom: 1.5rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.35);
}
.hero h1 { color: #ffffff; font-size: 2rem; font-weight: 800; margin: 0; }
.hero p { color: #cdd8ec; font-size: 1.05rem; margin: .4rem 0 0 0; }

.card {
    background: #171B26; border: 1px solid #2A3148; border-radius: 14px;
    padding: 1.3rem 1.4rem; height: 100%;
}
.card h4 { color: #7FA8F5; margin: 0 0 .4rem 0; font-size: 1.0rem; }
.card p { color: #A8B3C7; margin: 0; font-size: .92rem; }

.badge { display:inline-block; background:#2E4A7A; color:#DCE6FA; padding: 3px 10px;
    border-radius: 20px; font-size: .78rem; font-weight: 600; margin-right:6px; }

.metric-card { background:#171B26; border:1px solid #2A3148; border-radius:12px;
    padding: 1rem 1.2rem; text-align:center; }
.metric-card .val { font-size: 1.9rem; font-weight:800; color:#ffffff; }
.metric-card .lbl { font-size: .82rem; color:#8A94AB; text-transform:uppercase; letter-spacing:.05em; }

section[data-testid="stSidebar"] { background: #10141F; border-right: 1px solid #232838; }
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #B4650A, #D97C1A); border: none; font-weight: 700;
    border-radius: 10px; padding: .6rem 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---- Hero header ----
st.markdown("""
<div class="hero">
  <h1>Evidence-Aware Investigation Assistant</h1>
  <p>Upload case evidence and generate a fully cited, traceable investigator report.</p>
</div>
""", unsafe_allow_html=True)

# ---- Sidebar ----
st.sidebar.markdown("### 📁 Case Data")
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

with st.sidebar.expander("🕐 Preview Timeline", expanded=False):
    try:
        timeline = build_timeline(evidence_file)
        if len(timeline) == 0:
            st.write("No evidence items found.")
        for event in timeline:
            st.markdown(f"**{event['time']}** &nbsp; `{event['source_type']}`  \n{event['event']}")
    except Exception as e:
        st.error(f"Could not load timeline: {e}")

st.sidebar.markdown("---")
run_clicked = st.sidebar.button("▶  Run Pipeline: Generate Report", type="primary", use_container_width=True)

# ---- Main area ----
if run_clicked:
    try:
        with st.spinner("Retrieving evidence, correlating, and generating report..."):
            report = generate_report(evidence_file)

        cited = extract_citations(report)
        valid = get_valid_evidence_ids(evidence_file)
        invalid = cited - valid
        unused = valid - cited

        col1, col2, col3 = st.columns(3)
        for col, val, lbl in [(col1, len(cited), "Citations Used"),
                               (col2, len(invalid), "Invalid Citations"),
                               (col3, len(unused), "Uncited Evidence")]:
            with col:
                st.markdown(f'<div class="metric-card"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown("")
        tab1, tab2 = st.tabs(["📄  Report", "🔍  Citation Verification"])
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
    st.markdown("#### How it works")
    c1, c2, c3 = st.columns(3)
    cards = [
        ("🧩 Ingest & Correlate", "Evidence is normalized and linked into a knowledge graph across sources."),
        ("🎯 Evidence-Aware Retrieval", "Ranked by relevance, source reliability, and cross-source corroboration."),
        ("📌 Cited Generation", "Every claim in the final report traces back to a specific evidence ID."),
    ]
    for col, (title, desc) in zip([c1, c2, c3], cards):
        with col:
            st.markdown(f'<div class="card"><h4>{title}</h4><p>{desc}</p></div>', unsafe_allow_html=True)
    st.markdown("")
    st.info("👈  Click **Run Pipeline** in the sidebar to generate an investigator report.")