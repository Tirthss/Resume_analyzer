
import streamlit as st
import tempfile
import os
import time

from extractor import extract_text
from analyzer  import analyze
from database  import save_analysis, get_all_analyses, get_statistics, create_tables

# Initialize database
create_tables()

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="SmartATS — AI Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global */
    * { font-family: 'Inter', sans-serif; }

    /* Hide default streamlit elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a0f1e 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b2a 0%, #111827 100%);
        border-right: 1px solid #1e3a5f;
    }

    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #111827 0%, #1a2535 100%);
        border: 1px solid #1e3a5f;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); }

    .metric-value {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00b4d8, #90e0ef);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }

    .metric-label {
        font-size: 0.85rem;
        color: #8892a4;
        font-weight: 500;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #0d1b2a 0%, #111827 100%);
        border: 1px solid #1e3a5f;
        border-radius: 24px;
        padding: 48px 40px;
        text-align: center;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.2;
        margin-bottom: 12px;
    }

    .hero-accent {
        background: linear-gradient(135deg, #00b4d8, #90e0ef);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #8892a4;
        max-width: 560px;
        margin: 0 auto 24px;
        line-height: 1.6;
    }

    /* Score circle */
    .score-circle {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        font-weight: 800;
        box-shadow: 0 0 40px rgba(0,180,216,0.3);
    }

    /* Skill tags */
    .skill-tag-green {
        display: inline-block;
        background: rgba(6, 214, 160, 0.15);
        color: #06d6a0;
        border: 1px solid rgba(6, 214, 160, 0.3);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 3px;
    }

    .skill-tag-red {
        display: inline-block;
        background: rgba(239, 35, 60, 0.15);
        color: #ef233c;
        border: 1px solid rgba(239, 35, 60, 0.3);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 3px;
    }

    /* Section headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #111827, #1a2535);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }

    /* Steps */
    .step-card {
        background: linear-gradient(135deg, #111827, #1a2535);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        height: 100%;
    }

    .step-number {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #00b4d8, #0077b6);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.1rem;
        color: white;
        margin: 0 auto 12px;
    }

    /* Result section */
    .result-container {
        background: linear-gradient(135deg, #111827, #1a2535);
        border: 1px solid #00b4d8;
        border-radius: 20px;
        padding: 32px;
        margin-top: 24px;
        box-shadow: 0 0 40px rgba(0,180,216,0.1);
    }

    /* Progress bar custom */
    .progress-container {
        background: #1e3a5f;
        border-radius: 10px;
        height: 12px;
        margin: 8px 0;
        overflow: hidden;
    }

    /* Rec card */
    .rec-card {
        background: rgba(0,180,216,0.08);
        border: 1px solid rgba(0,180,216,0.2);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00b4d8, #0077b6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 12px 24px !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 20px rgba(0,180,216,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(0,180,216,0.5) !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #111827, #1a2535) !important;
        border: 2px dashed #1e3a5f !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }

    /* Text area */
    .stTextArea > div > div > textarea {
        background: #111827 !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 0.9rem !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #111827 !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* Divider */
    hr {
        border-color: #1e3a5f !important;
        margin: 24px 0 !important;
    }

    /* Badge */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-teal { background: rgba(0,180,216,0.15); color: #00b4d8; border: 1px solid rgba(0,180,216,0.3); }
    .badge-green { background: rgba(6,214,160,0.15); color: #06d6a0; border: 1px solid rgba(6,214,160,0.3); }
    .badge-orange { background: rgba(255,159,28,0.15); color: #ff9f1c; border: 1px solid rgba(255,159,28,0.3); }
    .badge-red { background: rgba(239,35,60,0.15); color: #ef233c; border: 1px solid rgba(239,35,60,0.3); }

</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0;'>
        <div style='font-size:2.5rem;'>🎯</div>
        <div style='font-size:1.4rem; font-weight:800; color:#ffffff; margin-top:8px;'>Smart<span style='color:#00b4d8;'>ATS</span></div>
        <div style='font-size:0.75rem; color:#8892a4; margin-top:4px;'>AI Resume Analyzer</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["🏠 Home", "🔍 Analyze Resume", "📊 Dashboard & History", "ℹ️ How It Works"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Stats in sidebar
    try:
        stats = get_statistics()
        st.markdown("""<div style='color:#8892a4; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:12px;'>LIVE STATS</div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class='metric-card' style='padding:12px;'>
                <div style='font-size:1.4rem; font-weight:800; color:#00b4d8;'>{stats['total']}</div>
                <div style='font-size:0.7rem; color:#8892a4;'>Analyses</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class='metric-card' style='padding:12px;'>
                <div style='font-size:1.4rem; font-weight:800; color:#06d6a0;'>{stats['avg_score']}%</div>
                <div style='font-size:0.7rem; color:#8892a4;'>Avg Score</div>
            </div>""", unsafe_allow_html=True)
    except:
        pass

    st.markdown("---")
    st.markdown("""
    <div style='color:#8892a4; font-size:0.75rem; text-align:center;'>
        Built using Python<br>
        ML Model: LinearSVC · 85.73% accuracy<br>
        46 Job Categories
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE: HOME
# ════════════════════════════════════════════════════════════
if page == "🏠 Home":

    # Hero
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>Know Where Your Resume<br><span class='hero-accent'>Actually Stands</span></div>
        <div class='hero-subtitle'>Upload your resume, paste any job description, and get instant AI-powered feedback — ATS score, skill gaps, and personalized recommendations.</div>
        <div style='display:flex; justify-content:center; gap:12px; flex-wrap:wrap;'>
            <span class='badge badge-teal'>🤖 Machine Learning</span>
            <span class='badge badge-green'>📄 5 File Formats</span>
            <span class='badge badge-orange'>🎯 46 Job Categories</span>
            <span class='badge badge-red'>⚡ Instant Results</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    col1, col2, col3, col4 = st.columns(4)
    stats_data = [
        ("4,867", "Resumes Trained", "🧠"),
        ("85.73%", "Model Accuracy", "🎯"),
        ("46", "Job Categories", "💼"),
        ("500ms", "Analysis Speed", "⚡"),
    ]
    for col, (val, label, icon) in zip([col1, col2, col3, col4], stats_data):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:1.8rem; margin-bottom:4px;'>{icon}</div>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # How it works
    st.markdown("<div class='section-header'>🚀 How It Works</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    steps = [
        ("1", "📤", "Upload Resume", "Upload TXT, DOCX, PDF, PNG or JPG format"),
        ("2", "📋", "Paste Job Description", "Copy the job description you're applying for"),
        ("3", "🤖", "AI Analysis", "Our ML model analyzes and scores your resume"),
        ("4", "📊", "Get Results", "See your score, skills, and improvement tips"),
    ]
    for col, (num, icon, title, desc) in zip([c1, c2, c3, c4], steps):
        with col:
            st.markdown(f"""
            <div class='step-card'>
                <div class='step-number'>{num}</div>
                <div style='font-size:1.8rem; margin-bottom:8px;'>{icon}</div>
                <div style='font-weight:700; color:#ffffff; margin-bottom:6px;'>{title}</div>
                <div style='font-size:0.82rem; color:#8892a4; line-height:1.5;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ATS Score Guide
    st.markdown("<div class='section-header'>📊 ATS Score Guide</div>", unsafe_allow_html=True)
    g1, g2, g3, g4 = st.columns(4)
    grades = [
        ("🟢", "75% - 100%", "Excellent Match", "Strong candidate — apply confidently!", "#06d6a0"),
        ("🟡", "60% - 75%", "Good Match", "Good fit — minor improvements needed", "#ff9f1c"),
        ("🟠", "45% - 60%", "Moderate Match", "Partial fit — add more keywords", "#f97316"),
        ("🔴", "0% - 45%", "Weak Match", "Needs significant improvement", "#ef233c"),
    ]
    for col, (emoji, score, verdict, tip, color) in zip([g1, g2, g3, g4], grades):
        with col:
            st.markdown(f"""
            <div class='metric-card' style='border-color:{color}40;'>
                <div style='font-size:1.5rem; margin-bottom:8px;'>{emoji}</div>
                <div style='font-size:1.2rem; font-weight:800; color:{color};'>{score}</div>
                <div style='font-weight:700; color:#ffffff; margin:6px 0;'>{verdict}</div>
                <div style='font-size:0.8rem; color:#8892a4;'>{tip}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # CTA
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0d1b2a, #111827); border: 1px solid #00b4d8; border-radius: 20px; padding: 32px; text-align: center;'>
        <div style='font-size:1.6rem; font-weight:800; color:#ffffff; margin-bottom:8px;'>Ready to Analyze Your Resume?</div>
        <div style='color:#8892a4; margin-bottom:16px;'>Click "Analyze Resume" in the sidebar to get started</div>
        <span class='badge badge-teal'>Free · No Login Required · Instant Results</span>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE: ANALYZE RESUME
# ════════════════════════════════════════════════════════════
elif page == "🔍 Analyze Resume":

    st.markdown("""
    <div style='margin-bottom:24px;'>
        <div style='font-size:2rem; font-weight:800; color:#ffffff;'>🔍 Analyze Your Resume</div>
        <div style='color:#8892a4; margin-top:4px;'>Upload your resume and paste the job description to get your ATS score</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#111827,#1a2535); border:1px solid #1e3a5f; border-radius:16px; padding:24px; margin-bottom:16px;'>
            <div style='font-size:1.1rem; font-weight:700; color:#ffffff; margin-bottom:4px;'>📎 Upload Resume</div>
            <div style='font-size:0.82rem; color:#8892a4;'>Supported: TXT, DOCX, PDF, PNG, JPG</div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Drop your resume here",
            type=["txt", "docx", "pdf", "png", "jpg", "jpeg"],
            label_visibility="collapsed"
        )

        if uploaded_file:
            file_size = uploaded_file.size / 1024
            st.markdown(f"""
            <div style='background:rgba(6,214,160,0.1); border:1px solid rgba(6,214,160,0.3); border-radius:10px; padding:12px; margin-top:8px;'>
                <span style='color:#06d6a0; font-weight:600;'>✅ File ready:</span>
                <span style='color:#e2e8f0; margin-left:8px;'>{uploaded_file.name}</span>
                <span style='color:#8892a4; margin-left:8px; font-size:0.8rem;'>({file_size:.1f} KB)</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#111827,#1a2535); border:1px solid #1e3a5f; border-radius:16px; padding:24px; margin-bottom:16px;'>
            <div style='font-size:1.1rem; font-weight:700; color:#ffffff; margin-bottom:4px;'>📋 Job Description</div>
            <div style='font-size:0.82rem; color:#8892a4;'>Paste the job posting you're applying for</div>
        </div>
        """, unsafe_allow_html=True)

        job_description = st.text_area(
            "Paste job description",
            height=200,
            placeholder="We are looking for a Full Stack Developer with React, Node.js, PostgreSQL experience...",
            label_visibility="collapsed"
        )

        if job_description:
            word_count = len(job_description.split())
            quality = "Excellent" if word_count > 100 else "Good" if word_count > 50 else "Add more detail"
            color = "#06d6a0" if word_count > 100 else "#ff9f1c" if word_count > 50 else "#ef233c"
            st.markdown(f"""
            <div style='color:{color}; font-size:0.82rem; margin-top:6px;'>
                📝 {word_count} words · Quality: {quality}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Analyze My Resume Now", use_container_width=True)

    if analyze_btn:
        if not uploaded_file:
            st.markdown("""
            <div style='background:rgba(239,35,60,0.1); border:1px solid rgba(239,35,60,0.3); border-radius:10px; padding:12px;'>
                ❌ Please upload a resume file first.
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        if not job_description.strip():
            st.markdown("""
            <div style='background:rgba(239,35,60,0.1); border:1px solid rgba(239,35,60,0.3); border-radius:10px; padding:12px;'>
                ❌ Please paste a job description.
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        # Progress animation
        progress_bar = st.progress(0)
        status = st.empty()

        steps_list = [
            (20, "📄 Extracting text from resume..."),
            (40, "🧹 Cleaning and preprocessing text..."),
            (60, "🤖 Running ML model for category prediction..."),
            (80, "📊 Calculating ATS score with cosine similarity..."),
            (95, "🎯 Matching skills and generating recommendations..."),
            (100, "✅ Analysis complete!")
        ]

        suffix = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        try:
            for prog, msg in steps_list:
                progress_bar.progress(prog)
                status.markdown(f"<div style='color:#00b4d8; font-size:0.9rem;'>{msg}</div>", unsafe_allow_html=True)
                time.sleep(0.3)

            resume_text = extract_text(tmp_path)

            if not resume_text.strip():
                st.error("Could not extract text. Please try a different file format.")
                st.stop()

            results = analyze(resume_text, job_description)

            save_analysis(
                filename=uploaded_file.name,
                category=results['category'],
                ats_score=results['ats_score'],
                verdict=results['verdict'],
                matched_skills=results['matched_skills'],
                missing_skills=results['missing_skills'],
                job_description=job_description
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()
        finally:
            os.remove(tmp_path)

        progress_bar.empty()
        status.empty()

        # ── RESULTS ──────────────────────────────────────────
        score = results['ats_score']
        verdict = results['verdict']
        category = results['category']

        # Score color
        if score >= 75:
            score_color = "#06d6a0"
            verdict_emoji = "🟢"
        elif score >= 60:
            score_color = "#ff9f1c"
            verdict_emoji = "🟡"
        elif score >= 45:
            score_color = "#f97316"
            verdict_emoji = "🟠"
        else:
            score_color = "#ef233c"
            verdict_emoji = "🔴"

        # Success banner
        st.markdown(f"""
        <div style='background:rgba(6,214,160,0.08); border:1px solid rgba(6,214,160,0.3); border-radius:16px; padding:20px; text-align:center; margin-bottom:24px;'>
            <div style='font-size:1.2rem; font-weight:700; color:#06d6a0;'>✅ Analysis Complete!</div>
            <div style='color:#8892a4; font-size:0.85rem; margin-top:4px;'>Results saved to database</div>
        </div>
        """, unsafe_allow_html=True)

        # Main metrics
        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(f"""
            <div class='metric-card' style='border-color:{score_color}40;'>
                <div style='font-size:0.8rem; color:#8892a4; margin-bottom:8px; text-transform:uppercase;'>ATS Match Score</div>
                <div style='font-size:3.5rem; font-weight:800; color:{score_color};'>{score}%</div>
                <div style='margin-top:8px;'>
                    <div style='background:#1e3a5f; border-radius:10px; height:8px; overflow:hidden;'>
                        <div style='background:{score_color}; width:{score}%; height:100%; border-radius:10px; transition:width 1s;'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:0.8rem; color:#8892a4; margin-bottom:8px; text-transform:uppercase;'>Predicted Category</div>
                <div style='font-size:1.3rem; font-weight:800; color:#00b4d8; line-height:1.3;'>{category.replace("-", " ")}</div>
                <div style='margin-top:12px;'><span class='badge badge-teal'>🤖 AI Predicted</span></div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class='metric-card' style='border-color:{score_color}40;'>
                <div style='font-size:0.8rem; color:#8892a4; margin-bottom:8px; text-transform:uppercase;'>Verdict</div>
                <div style='font-size:1.8rem; font-weight:800; color:{score_color};'>{verdict_emoji} {verdict}</div>
                <div style='margin-top:8px; font-size:0.8rem; color:#8892a4;'>
                    {'Apply confidently! 🚀' if score >= 75 else 'Minor improvements needed 💡' if score >= 60 else 'Add more keywords 📝' if score >= 45 else 'Needs significant work 🔧'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Skills
        sk1, sk2 = st.columns(2)

        with sk1:
            matched = results['matched_skills']
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#111827,#1a2535); border:1px solid rgba(6,214,160,0.3); border-radius:16px; padding:24px;'>
                <div style='font-size:1.1rem; font-weight:700; color:#06d6a0; margin-bottom:16px;'>
                    ✅ Matched Skills <span style='background:rgba(6,214,160,0.15); color:#06d6a0; border-radius:20px; padding:2px 10px; font-size:0.8rem; margin-left:8px;'>{len(matched)}</span>
                </div>
                <div>
                    {''.join([f"<span class='skill-tag-green'>{s.title()}</span>" for s in matched]) if matched else "<span style='color:#8892a4;'>No matching skills found</span>"}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with sk2:
            missing = results['missing_skills']
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#111827,#1a2535); border:1px solid rgba(239,35,60,0.3); border-radius:16px; padding:24px;'>
                <div style='font-size:1.1rem; font-weight:700; color:#ef233c; margin-bottom:16px;'>
                    ❌ Missing Skills <span style='background:rgba(239,35,60,0.15); color:#ef233c; border-radius:20px; padding:2px 10px; font-size:0.8rem; margin-left:8px;'>{len(missing)}</span>
                </div>
                <div>
                    {''.join([f"<span class='skill-tag-red'>{s.title()}</span>" for s in missing]) if missing else "<span style='color:#06d6a0;'>🎉 You have all required skills!</span>"}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Recommendations
        st.markdown("""
        <div style='font-size:1.1rem; font-weight:700; color:#ffffff; margin-bottom:16px;'>💡 Personalized Recommendations</div>
        """, unsafe_allow_html=True)

        for i, rec in enumerate(results['recommendations'], 1):
            st.markdown(f"""
            <div class='rec-card'>
                <span style='color:#00b4d8; font-weight:700; margin-right:8px;'>{i}.</span>
                <span style='color:#e2e8f0;'>{rec}</span>
            </div>
            """, unsafe_allow_html=True)

        # Extracted text
        with st.expander("🔍 View Extracted Resume Text"):
            st.markdown(f"""
            <div style='background:#111827; border-radius:10px; padding:16px; color:#8892a4; font-size:0.82rem; font-family:monospace; line-height:1.6;'>
                {resume_text[:3000]}{'...' if len(resume_text) > 3000 else ''}
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE: DASHBOARD & HISTORY
# ════════════════════════════════════════════════════════════
elif page == "📊 Dashboard & History":

    st.markdown("""
    <div style='margin-bottom:24px;'>
        <div style='font-size:2rem; font-weight:800; color:#ffffff;'>📊 Dashboard & History</div>
        <div style='color:#8892a4; margin-top:4px;'>All your analyses stored in SQLite database</div>
    </div>
    """, unsafe_allow_html=True)

    stats = get_statistics()

    # Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='metric-card'><div class='metric-value'>{stats['total']}</div><div class='metric-label'>Total Analyses</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card'><div class='metric-value'>{stats['avg_score']}%</div><div class='metric-label'>Average Score</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card'><div class='metric-value'>{stats['excellent']}</div><div class='metric-label'>Excellent Matches</div></div>""", unsafe_allow_html=True)
    with c4:
        top = stats['top_category'].replace('-', ' ') if stats['top_category'] != 'N/A' else 'N/A'
        st.markdown(f"""<div class='metric-card'><div style='font-size:1.1rem; font-weight:800; color:#00b4d8;'>{top}</div><div class='metric-label'>Top Category</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Score distribution
    st.markdown("<div class='section-header'>🎯 Score Distribution</div>", unsafe_allow_html=True)
    d1, d2, d3, d4 = st.columns(4)
    dist = [
        ("🟢", "Excellent", stats['excellent'], "#06d6a0"),
        ("🟡", "Good", stats['good'], "#ff9f1c"),
        ("🟠", "Moderate", stats['moderate'], "#f97316"),
        ("🔴", "Weak", stats['weak'], "#ef233c"),
    ]
    for col, (emoji, label, count, color) in zip([d1, d2, d3, d4], dist):
        with col:
            st.markdown(f"""
            <div class='metric-card' style='border-color:{color}40;'>
                <div style='font-size:1.5rem;'>{emoji}</div>
                <div style='font-size:1.8rem; font-weight:800; color:{color};'>{count}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # History table
    st.markdown("<div class='section-header'>📋 Analysis History</div>", unsafe_allow_html=True)
    rows = get_all_analyses()

    if not rows:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#111827,#1a2535); border:1px solid #1e3a5f; border-radius:16px; padding:40px; text-align:center;'>
            <div style='font-size:2rem; margin-bottom:12px;'>📭</div>
            <div style='color:#ffffff; font-weight:700; margin-bottom:8px;'>No analyses yet</div>
            <div style='color:#8892a4;'>Go to Analyze Resume to get started!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        import pandas as pd
        data = []
        for row in rows:
            score = row['ats_score']
            verdict_emoji = "🟢" if score >= 75 else "🟡" if score >= 60 else "🟠" if score >= 45 else "🔴"
            data.append({
                'ID': row['id'],
                'File': row['filename'],
                'Category': row['predicted_category'].replace('-', ' '),
                'ATS Score': f"{score}%",
                'Verdict': f"{verdict_emoji} {row['verdict']}",
                'Matched Skills': row['matched_skills'][:50] + '...' if row['matched_skills'] and len(row['matched_skills']) > 50 else row['matched_skills'],
                'Date': row['analyzed_at']
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div style='color:#8892a4; font-size:0.8rem; margin-top:8px;'>
            📦 Data stored in: <code>resume_analyzer.db</code> (SQLite Database) · {len(data)} records
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE: HOW IT WORKS
# ════════════════════════════════════════════════════════════
elif page == "ℹ️ How It Works":

    st.markdown("""
    <div style='margin-bottom:24px;'>
        <div style='font-size:2rem; font-weight:800; color:#ffffff;'>ℹ️ How SmartATS Works</div>
        <div style='color:#8892a4; margin-top:4px;'>The technology behind your resume analysis</div>
    </div>
    """, unsafe_allow_html=True)

    # Pipeline
    st.markdown("<div class='section-header'>🔄 Analysis Pipeline</div>", unsafe_allow_html=True)

    pipeline = [
        ("1", "📄", "Text Extraction", "TXT files read directly. DOCX parsed with python-docx. PDF text extracted with pdfplumber. Images processed with Tesseract OCR after preprocessing (grayscale, contrast boost, sharpen, 2x resize).", "#00b4d8"),
        ("2", "🧹", "NLP Preprocessing", "Text lowercased, URLs/emails removed, punctuation stripped, tokenized with NLTK word_tokenize, stopwords filtered (179 common English words), short words removed.", "#06d6a0"),
        ("3", "📊", "TF-IDF Vectorization", "Cleaned text converted to 10,000-dimensional sparse vector. Bigrams capture two-word phrases like 'machine learning'. Sublinear TF scaling prevents frequency dominance.", "#ff9f1c"),
        ("4", "🤖", "ML Classification", "LinearSVC trained on 4,867 balanced resumes across 46 categories. Finds optimal hyperplane in 10,000D space. CalibratedClassifierCV adds probability scores.", "#7b2d8b"),
        ("5", "📐", "Cosine Similarity", "Both resume and job description converted to TF-IDF vectors. Cosine of angle between vectors = ATS score. Length-independent measurement of textual similarity.", "#ef233c"),
        ("6", "🎯", "Skill Matching", "50+ technical skills checked against both texts. Set intersection = matched skills. Set difference = missing skills. Generates prioritized recommendations.", "#f97316"),
    ]

    for num, icon, title, desc, color in pipeline:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#111827,#1a2535); border:1px solid {color}30; border-left:4px solid {color}; border-radius:12px; padding:20px; margin-bottom:12px; display:flex; gap:16px;'>
            <div style='background:{color}20; border-radius:50%; width:44px; height:44px; display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:1.3rem;'>{icon}</div>
            <div>
                <div style='font-weight:700; color:{color}; margin-bottom:4px;'>Step {num}: {title}</div>
                <div style='color:#8892a4; font-size:0.88rem; line-height:1.6;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Model details
    st.markdown("<div class='section-header'>🤖 ML Model Details</div>", unsafe_allow_html=True)
    mc1, mc2 = st.columns(2)

    with mc1:
        st.markdown("""
        <div class='info-box'>
            <div style='font-weight:700; color:#00b4d8; margin-bottom:12px;'>LinearSVC Model</div>
            <div style='color:#8892a4; font-size:0.88rem; line-height:1.8;'>
                • Algorithm: Linear Support Vector Classifier<br>
                • Training data: 4,867 balanced resumes<br>
                • Categories: 46 job types<br>
                • Features: 10,000 TF-IDF bigram features<br>
                • C parameter: 1.0 (balanced regularization)<br>
                • Probability: CalibratedClassifierCV (cv=3)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with mc2:
        st.markdown("""
        <div class='info-box'>
            <div style='font-weight:700; color:#06d6a0; margin-bottom:12px;'>Performance Metrics</div>
            <div style='color:#8892a4; font-size:0.88rem; line-height:1.8;'>
                • Accuracy: 85.73%<br>
                • Precision: 86.42%<br>
                • Recall: 85.73%<br>
                • F1 Score: 85.76%<br>
                • Cross Validation: 5-fold consistent<br>
                • vs Random guessing (46 classes): 2.17%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Tech stack
    st.markdown("<br><div class='section-header'>🛠️ Tech Stack</div>", unsafe_allow_html=True)
    tc1, tc2, tc3 = st.columns(3)

    techs = [
        ("Frontend", [("Streamlit", "Python web framework"), ("HTML/CSS", "Custom styling"), ("Plotly", "Visualizations")], "#00b4d8"),
        ("Backend & ML", [("scikit-learn", "LinearSVC + TF-IDF"), ("NLTK", "NLP preprocessing"), ("pickle", "Model serialization")], "#06d6a0"),
        ("File & Data", [("Tesseract OCR", "Image text extraction"), ("pdfplumber", "PDF parsing"), ("SQLite", "Database storage")], "#ff9f1c"),
    ]

    for col, (title, items, color) in zip([tc1, tc2, tc3], techs):
        with col:
            items_html = ''.join([f"<div style='padding:6px 0; border-bottom:1px solid #1e3a5f;'><span style='color:{color}; font-weight:600;'>{name}</span><br><span style='color:#8892a4; font-size:0.8rem;'>{desc}</span></div>" for name, desc in items])
            st.markdown(f"""
            <div class='info-box'>
                <div style='font-weight:700; color:{color}; margin-bottom:12px;'>{title}</div>
                {items_html}
            </div>
            """, unsafe_allow_html=True)
