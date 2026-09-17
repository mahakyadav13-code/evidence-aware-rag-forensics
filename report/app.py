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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero {
    background: radial-gradient(circle at 15% 20%, #2E4A7A 0%, #10141F 55%), 
                linear-gradient(135deg, #1a2b4c, #0B0E17);
    padding: 2.4rem 2.6rem; border-radius: 18px; margin-bottom: 1.4rem;
    border: 1px solid #2A3148; position: relative; overflow: hidden;
}
.hero::before { content: "⛓"; position:absolute; right:2rem; top:1.5rem; font-size:5rem; opacity:0.06; }
.hero h1 { color: #ffffff; font-size: 2.1rem; font-weight: 800; margin: 0; }
.hero p { color: #A9B7D6; font-size: 1.05rem; margin: .5rem 0 0 0; }
.hero .tagline { color: #D97C1A; font-family:'JetBrains Mono', monospace; font-size:.82rem; letter-spacing:.08em; text-transform:uppercase; margin-bottom:.5rem;}

.card {
    background: #141925; border: 1px solid #232A3D; border-radius: 14px;
    padding: 1.3rem 1.4rem; height: 100%; transition: border-color .2s;
}
.card:hover { border-color: #D97C1A; }
.card h4 { color: #7FA8F5; margin: 0 0 .4rem 0; font-size: 1.0rem; }
.card p { color: #9AA5BD; margin: 0; font-size: .9rem; line-height:1.5; }

.stat-strip { display:flex; gap:12px; margin: 1rem 0 1.6rem 0; }
.stat-box { flex:1; background:#141925; border:1px solid #232A3D; border-radius:12px; padding:.9rem 1rem; }
.stat-box .num { font-size:1.5rem; font-weight:800; color:#fff; }
.stat-box .lbl { font-size:.75rem; color:#7B8398; text-transform:uppercase; letter-spacing:.06em; }

.metric-card { background:#141925; border:1px solid #232A3D; border-radius:12px;
    padding: 1.1rem 1.2rem; text-align:center; }
.metric-card .val { font-size: 2rem; font-weight:800; color:#ffffff; }
.metric-card .lbl { font-size: .8rem; color:#7B8398; text-transform:uppercase; letter-spacing:.05em; }

.badge { display:inline-block; background:#1D2A44; color:#9FC0FF; border:1px solid #2E4A7A; 
    padding: 3px 10px; border-radius: 20px; font-size: .76rem; font-family:'JetBrains Mono',monospace; margin:2px; }

footer-note { color:#5B6478; font-size:.8rem; }

section[data-testid="stSidebar"] { background: #0D111A; border-right: 1px solid #1E2334; }
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #D97C1A, #B4650A); border: none; font-weight: 700;
    border-radius: 10px; padding: .65rem 1rem; box-shadow: 0 4px 14px rgba(217,124,26,0.35);
}
</style>
""", unsafe_allow_html=True)

# ---- Hero ----
default_path = "synthetic_case_v0/evidence.json"
try:
    with open(default_path) as f:
        n_items = len(json.load(f))
except Exception:
    n_items = "—"

st.markdown(f"""
<div class="hero">
  <div class="tagline">Digital Forensics · Knowledge Graphs · Retrieval-Augmented Generation</div>
  <h1>Evidence-Aware Investigation Assistant</h1>
  <p>Correlates heterogeneous digital evidence into a knowledge graph, retrieves it with 
  reliability-aware ranking, and generates investigator reports where every claim cites 
  its source.</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="stat-strip">
  <div class="stat-box"><div class="num">{n_items}</div><div class="lbl">Evidence Items Loaded</div></div>
  <div class="stat-box"><div class="num">5</div><div class="lbl">Evidence Types Supported</div></div>
  <div class="stat-box"><div class="num">Hybrid</div><div class="lbl">Retrieval Strategy</div></div>
  <div class="stat-box"><div class="num">100%</div><div class="lbl">Citation-Traceable</div></div>
</div>
""", unsafe_allow_html=True)

# ---- Sidebar ----
st.sidebar.markdown("### 📁 Case Data")
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
st.sidebar.caption("Evidence-Aware RAG · Cybercrime Investigation Framework · v1.0")

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
            if cited:
                badges = " ".join([f'<span class="badge">{c}</span>' for c in sorted(cited)])
                st.markdown(f"**Cited evidence:** {badges}", unsafe_allow_html=True)
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

st.markdown("<br><hr style='border-color:#1E2334'>", unsafe_allow_html=True)
st.markdown("<span style='color:#5B6478; font-size:.8rem;'>Evidence-Aware RAG Framework for Automated Cybercrime Investigation — 4th Year Research Project</span>", unsafe_allow_html=True)