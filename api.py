# ============================================================
# api.py - FastAPI Backend
# This replaces Streamlit for the Lovable frontend connection
# RUN: uvicorn api:app --reload
# ============================================================

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile, os, shutil

from extractor import extract_text
from analyzer  import analyze
from database  import save_analysis, get_all_analyses, get_statistics, create_tables

app = FastAPI(title="AI Resume Analyzer API")

# ── CORS — allows Lovable frontend to call this API ──────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production replace * with your Lovable URL
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()

@app.get("/")
def root():
    return {"message": "AI Resume Analyzer API is running!"}


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),           # uploaded resume file
    job_description: str = Form(...)        # job description text
):
    """
    Main endpoint. Accepts resume file + job description.
    Returns ATS score, category, skills, recommendations.
    """
    # Save uploaded file temporarily
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # Extract text from file
        resume_text = extract_text(tmp_path)

        if not resume_text.strip():
            return {"error": "Could not extract text from file"}

        # Run analysis
        results = analyze(resume_text, job_description)

        # Save to database
        save_analysis(
            filename        = file.filename,
            category        = results['category'],
            ats_score       = results['ats_score'],
            verdict         = results['verdict'],
            matched_skills  = results['matched_skills'],
            missing_skills  = results['missing_skills'],
            job_description = job_description
        )

        return {
            "success"        : True,
            "filename"       : file.filename,
            "category"       : results['category'],
            "ats_score"      : results['ats_score'],
            "verdict"        : results['verdict'],
            "verdict_emoji"  : results['verdict_emoji'],
            "matched_skills" : results['matched_skills'],
            "missing_skills" : results['missing_skills'],
            "recommendations": results['recommendations'],
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        os.remove(tmp_path)


@app.get("/history")
def get_history():
    """Returns all past analyses from database."""
    rows = get_all_analyses()
    data = []
    for row in rows:
        data.append({
            "id"       : row["id"],
            "filename" : row["filename"],
            "category" : row["predicted_category"],
            "ats_score": row["ats_score"],
            "verdict"  : row["verdict"],
            "date"     : row["analyzed_at"],
        })
    return {"analyses": data}


@app.get("/stats")
def get_stats():
    """Returns statistics from database."""
    return get_statistics()
