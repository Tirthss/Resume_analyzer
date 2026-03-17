# ============================================================
# app.py
# JOB: The main Streamlit web app — this is what the user sees
#
# HOW TO RUN: streamlit run app.py
# ============================================================

import streamlit as st
import tempfile
import os

from extractor import extract_text   # reads file → text
from analyzer  import analyze        # text + JD → results

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ── TITLE ────────────────────────────────────────────────────
st.title("📄 AI-Based Resume Analyzer")
st.markdown("Upload your resume and paste a job description to get your **ATS match score**, matched skills, and improvement tips.")
st.divider()

# ── TWO COLUMNS: left = upload, right = job description ──────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📎 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Supported formats: TXT, DOCX, PNG, JPG",
        type=["txt", "docx", "png", "jpg", "jpeg"]
    )

with col2:
    st.subheader("📋 Paste Job Description")
    job_description = st.text_area(
        "Copy-paste the job description here",
        height=250,
        placeholder="e.g. We are looking for a Python developer with experience in machine learning..."
    )

st.divider()

# ── ANALYZE BUTTON ───────────────────────────────────────────
analyze_btn = st.button("🔍 Analyze Resume", use_container_width=True, type="primary")

if analyze_btn:

    # Validate inputs
    if not uploaded_file:
        st.error("Please upload a resume file.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()

    # Show a loading spinner while processing
    with st.spinner("Analyzing your resume... please wait ⏳"):

        # Save uploaded file to a temp location so we can read it
        suffix = os.path.splitext(uploaded_file.name)[1]   # e.g. ".pdf"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        try:
            # Step 1: Extract text from the file
            resume_text = extract_text(tmp_path)

            if not resume_text.strip():
                st.error("Could not extract text from the file. Try a different format.")
                st.stop()

            # Step 2: Run the full analysis
            results = analyze(resume_text, job_description)

        except FileNotFoundError as e:
            st.error(str(e))
            st.stop()
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()
        finally:
            os.remove(tmp_path)   # clean up temp file

    # ── RESULTS SECTION ──────────────────────────────────────
    st.success("Analysis complete!")
    st.divider()

    # ── ROW 1: Score + Category + Verdict ────────────────────
    m1, m2, m3 = st.columns(3)

    m1.metric(
        label="🎯 ATS Match Score",
        value=f"{results['ats_score']}%"
    )
    m2.metric(
        label="📂 Predicted Category",
        value=results['category']
    )
    m3.metric(
        label="📊 Verdict",
        value=f"{results['verdict_emoji']} {results['verdict']}"
    )

    st.divider()

    # ── ROW 2: Skills breakdown ───────────────────────────────
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
            st.success("You have all the required skills!")

    st.divider()

    # ── ROW 3: Recommendations ───────────────────────────────
    st.subheader("💡 Recommendations")
    for i, rec in enumerate(results['recommendations'], 1):
        st.markdown(f"**{i}.** {rec}")

    st.divider()

    # ── EXPANDABLE: Show extracted resume text ────────────────
    with st.expander("🔍 View Extracted Resume Text"):
        st.text(resume_text[:2000] + ("..." if len(resume_text) > 2000 else ""))
