# ============================================================
# analyzer.py
# JOB: Given resume text + job description, return:
#       1. Predicted category (Data Science, Web Dev, etc.)
#       2. ATS score (how well the resume matches the job)
#       3. Matched skills
#       4. Missing skills
#       5. Recommendations
# ============================================================

import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from cleaner import clean_text

# ── Common skills list used for skill matching ────────────────
SKILLS_LIST = [
    'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'r',
    'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'redis',
    'machine learning', 'deep learning', 'artificial intelligence',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn',
    'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn',
    'react', 'angular', 'vue', 'nodejs', 'django', 'flask',
    'aws', 'azure', 'gcp', 'google cloud', 'cloud computing',
    'docker', 'kubernetes', 'jenkins', 'ci/cd',
    'git', 'github', 'gitlab',
    'data analysis', 'data science', 'data visualization',
    'nlp', 'natural language processing', 'computer vision',
    'rest api', 'graphql', 'microservices',
    'agile', 'scrum', 'devops', 'leadership', 'communication',
    'html', 'css', 'bootstrap', 'tailwind',
    'linux', 'bash', 'excel', 'powerpoint', 'tableau', 'power bi'
]


def load_models():
    """
    Load the saved ML model, TF-IDF vectorizer, and label encoder.
    These were saved by train_model.py
    """
    try:
        model = pickle.load(open('models/model.pkl', 'rb'))
        tfidf = pickle.load(open('models/tfidf.pkl', 'rb'))
        le    = pickle.load(open('models/label_encoder.pkl', 'rb'))
        return model, tfidf, le
    except FileNotFoundError:
        raise FileNotFoundError(
            "Model files not found! Please run train_model.py first."
        )


def predict_category(resume_text, model, tfidf, le):
    """
    Predict what job category this resume belongs to.
    Example: "Data Science", "Java Developer", "HR", etc.
    """
    cleaned = clean_text(resume_text)
    vector  = tfidf.transform([cleaned])          # convert text to numbers
    prediction = model.predict(vector)            # predict the label (number)
    category = le.inverse_transform(prediction)  # number → category name
    return category[0]


def calculate_ats_score(resume_text, job_description):
    """
    Calculate how well the resume matches the job description.

    How it works:
    - Both texts are converted to TF-IDF vectors
    - Cosine similarity measures the angle between the two vectors
    - Closer angle = more similar = higher score
    - Score is returned as a percentage (0–100)
    """
    cleaned_resume = clean_text(resume_text)
    cleaned_job    = clean_text(job_description)

    # Build a fresh TF-IDF on just these two documents
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([cleaned_resume, cleaned_job])

    # cosine_similarity returns a value between 0 and 1
    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]

    return round(score * 100, 2)   # convert to percentage


def extract_skills(resume_text, job_description):
    """
    Compare skills found in the resume vs. skills required in the job.

    Returns a dict with:
      - resume_skills  : skills found in resume
      - job_skills     : skills required by job
      - matched_skills : skills in both (good!)
      - missing_skills : skills in job but NOT in resume (need to add)
    """
    resume_lower = resume_text.lower()
    job_lower    = job_description.lower()

    resume_skills = sorted(set(s for s in SKILLS_LIST if s in resume_lower))
    job_skills    = sorted(set(s for s in SKILLS_LIST if s in job_lower))

    matched_skills = sorted(set(resume_skills) & set(job_skills))
    missing_skills = sorted(set(job_skills) - set(resume_skills))

    return {
        'resume_skills' : resume_skills,
        'job_skills'    : job_skills,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
    }


def get_verdict(ats_score):
    """
    Return a human-readable verdict based on the ATS score.
    """
    if ats_score >= 75:
        return "Excellent Match", "🟢"
    elif ats_score >= 60:
        return "Good Match", "🟡"
    elif ats_score >= 45:
        return "Moderate Match", "🟠"
    else:
        return "Weak Match", "🔴"


def get_recommendations(ats_score, missing_skills, matched_skills):
    """
    Generate helpful suggestions based on the analysis results.
    """
    recs = []

    if missing_skills:
        top3 = ', '.join(missing_skills[:3])
        recs.append(f"Add these missing skills to your resume: {top3}")

    if ats_score < 60:
        recs.append("Use more keywords from the job description in your resume.")
        recs.append("Align your experience section with the job requirements.")

    if matched_skills:
        recs.append(f"Highlight these {len(matched_skills)} matching skills more prominently.")

    if not recs:
        recs.append("Great job! Your resume is well-matched to this position.")

    return recs


def analyze(resume_text, job_description):
    """
    MASTER FUNCTION — call this from app.py.

    Takes resume text + job description, runs everything,
    and returns a single results dictionary.
    """
    # Load models
    model, tfidf, le = load_models()

    # Run all analysis steps
    category  = predict_category(resume_text, model, tfidf, le)
    ats_score = calculate_ats_score(resume_text, job_description)
    skills    = extract_skills(resume_text, job_description)
    verdict, emoji = get_verdict(ats_score)
    recommendations = get_recommendations(
        ats_score, skills['missing_skills'], skills['matched_skills']
    )

    return {
        'category'       : category,
        'ats_score'      : ats_score,
        'verdict'        : verdict,
        'verdict_emoji'  : emoji,
        'matched_skills' : skills['matched_skills'],
        'missing_skills' : skills['missing_skills'],
        'resume_skills'  : skills['resume_skills'],
        'job_skills'     : skills['job_skills'],
        'recommendations': recommendations,
    }
