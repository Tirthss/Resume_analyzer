# ============================================================
# app.py - UPDATED WITH DATABASE CONNECTIVITY
# ============================================================

import streamlit as st
import tempfile
import os

from extractor import extract_text
from analyzer  import analyze
from database  import save_analysis, get_all_analyses, get_statistics, create_tables

# Initialize database on startup
create_tables()

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ── SIDEBAR NAVIGATION ───────────────────────────────────────
st.sidebar.title("📄 Resume Analyzer")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["🔍 Analyze Resume", "📊 History & Stats"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Tech Stack:**")
st.sidebar.markdown("- Python + Streamlit")
st.sidebar.markdown("- LinearSVC + TF-IDF")
st.sidebar.markdown("- SQLite Database")
st.sidebar.markdown("- Tesseract OCR")
st.sidebar.markdown("- NLTK NLP")

# ════════════════════════════════════════════════════════════
# PAGE 1: ANALYZE RESUME
# ════════════════════════════════════════════════════════════
if page == "🔍 Analyze Resume":

    st.title("📄 AI-Based Resume Analyzer")
    st.markdown("Upload your resume and paste a job description to get your **ATS match score**, matched skills, and improvement tips.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📎 Upload Your Resume")
        uploaded_file = st.file_uploader(
            "Supported formats: TXT, DOCX, PNG, PDF, JPG",
           type=["txt", "docx", "pdf", "png", "jpg", "jpeg"]
        )

    with col2:
        st.subheader("📋 Paste Job Description")
        job_description = st.text_area(
            "Copy-paste the job description here",
            height=250,
            placeholder="e.g. We are looking for a Python developer..."
        )

    st.divider()
    analyze_btn = st.button("🔍 Analyze Resume", use_container_width=True, type="primary")

    if analyze_btn:
        if not uploaded_file:
            st.error("Please upload a resume file.")
            st.stop()
        if not job_description.strip():
            st.error("Please paste a job description.")
            st.stop()

        with st.spinner("Analyzing your resume... please wait ⏳"):
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            try:
                resume_text = extract_text(tmp_path)

                if not resume_text.strip():
                    st.error("Could not extract text. Try a different format.")
                    st.stop()

                results = analyze(resume_text, job_description)

                # ── SAVE TO DATABASE ──────────────────────────
                save_analysis(
                    filename        = uploaded_file.name,
                    category        = results['category'],
                    ats_score       = results['ats_score'],
                    verdict         = results['verdict'],
                    matched_skills  = results['matched_skills'],
                    missing_skills  = results['missing_skills'],
                    job_description = job_description
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()
            finally:
                os.remove(tmp_path)

        # ── RESULTS ──────────────────────────────────────────
        st.success("✅ Analysis complete! Results saved to database.")
        st.divider()

        m1, m2, m3 = st.columns(3)
        m1.metric(label="🎯 ATS Match Score", value=f"{results['ats_score']}%")
        m2.metric(label="📂 Predicted Category", value=results['category'])
        m3.metric(label="📊 Verdict", value=f"{results['verdict_emoji']} {results['verdict']}")

        st.divider()

        skill_col1, skill_col2 = st.columns(2)

        with skill_col1:
            st.subheader("✅ Matched Skills")
            if results['matched_skills']:
                for skill in results['matched_skills']:
                    st.markdown(f"- {skill.title()}")
            else:
                st.info("No matching skills found.")

        with skill_col2:
            st.subheader("❌ Missing Skills")
            if results['missing_skills']:
                for skill in results['missing_skills']:
                    st.markdown(f"- {skill.title()}")
            else:
                st.success("You have all required skills!")

        st.divider()
        st.subheader("💡 Recommendations")
        for i, rec in enumerate(results['recommendations'], 1):
            st.markdown(f"**{i}.** {rec}")

        with st.expander("🔍 View Extracted Resume Text"):
            st.text(resume_text[:2000])

# ════════════════════════════════════════════════════════════
# PAGE 2: HISTORY & STATS
# ════════════════════════════════════════════════════════════
elif page == "📊 History & Stats":

    st.title("📊 Analysis History & Statistics")
    st.markdown("All resume analyses are stored in **SQLite database** and displayed here.")
    st.divider()

    # ── STATISTICS ───────────────────────────────────────────
    stats = get_statistics()

    st.subheader("📈 Overall Statistics")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Analyses", stats['total'])
    s2.metric("Average ATS Score", f"{stats['avg_score']}%")
    s3.metric("Top Category", stats['top_category'])
    s4.metric("Excellent Matches", stats['excellent'])

    st.divider()

    # Score distribution
    st.subheader("🎯 Score Distribution")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("🟢 Excellent (75%+)", stats['excellent'])
    d2.metric("🟡 Good (60-75%)", stats['good'])
    d3.metric("🟠 Moderate (45-60%)", stats['moderate'])
    d4.metric("🔴 Weak (<45%)", stats['weak'])

    st.divider()

    # ── HISTORY TABLE ─────────────────────────────────────────
    st.subheader("📋 Analysis History (from Database)")

    rows = get_all_analyses()

    if not rows:
        st.info("No analyses yet. Go to Analyze Resume page to get started!")
    else:
        import pandas as pd
        data = []
        for row in rows:
            data.append({
                'ID'           : row['id'],
                'File'         : row['filename'],
                'Category'     : row['predicted_category'],
                'ATS Score'    : f"{row['ats_score']}%",
                'Verdict'      : row['verdict'],
                'Matched Skills': row['matched_skills'],
                'Date'         : row['analyzed_at']
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

        st.caption(f"📦 Data stored in: resume_analyzer.db (SQLite Database)")
