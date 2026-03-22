# ============================================================
# database.py
# JOB: Handle all database operations using SQLite
#
# WHY SQLite?
# - Built into Python — no installation needed
# - Stores data permanently on disk
# - Perfect for small to medium applications
# - Industry standard for local database connectivity
# ============================================================

import sqlite3
import os
from datetime import datetime

# Database file will be created in project folder
DB_PATH = 'resume_analyzer.db'


def get_connection():
    """
    Create and return a connection to the SQLite database.
    If database file doesn't exist, SQLite creates it automatically.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # allows accessing columns by name
    return conn


def create_tables():
    """
    Create database tables if they don't exist.
    Called once when app starts.

    Table: analysis_results
    Stores every resume analysis performed by users.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            filename        TEXT NOT NULL,
            predicted_category TEXT NOT NULL,
            ats_score       REAL NOT NULL,
            verdict         TEXT NOT NULL,
            matched_skills  TEXT,
            missing_skills  TEXT,
            job_description TEXT,
            analyzed_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database tables created successfully!")


def save_analysis(filename, category, ats_score, verdict,
                  matched_skills, missing_skills, job_description):
    """
    Save one analysis result to the database.

    Parameters:
        filename        : name of uploaded resume file
        category        : predicted job category
        ats_score       : ATS match percentage
        verdict         : Excellent/Good/Moderate/Weak
        matched_skills  : list of matched skills
        missing_skills  : list of missing skills
        job_description : the job description used for analysis
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Convert lists to comma-separated strings for storage
    matched_str = ', '.join(matched_skills) if matched_skills else ''
    missing_str = ', '.join(missing_skills) if missing_skills else ''

    cursor.execute('''
        INSERT INTO analysis_results
        (filename, predicted_category, ats_score, verdict,
         matched_skills, missing_skills, job_description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (filename, category, ats_score, verdict,
          matched_str, missing_str, job_description[:500]))

    conn.commit()
    conn.close()
    print(f"Analysis saved to database: {filename} → {category} ({ats_score}%)")


def get_all_analyses():
    """
    Retrieve all analysis records from database.
    Returns list of rows ordered by most recent first.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, filename, predicted_category, ats_score,
               verdict, matched_skills, missing_skills, analyzed_at
        FROM analysis_results
        ORDER BY analyzed_at DESC
    ''')

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_statistics():
    """
    Get summary statistics from all analyses.
    Used for the History & Stats page.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Total analyses count
    cursor.execute('SELECT COUNT(*) as total FROM analysis_results')
    total = cursor.fetchone()['total']

    # Average ATS score
    cursor.execute('SELECT AVG(ats_score) as avg_score FROM analysis_results')
    avg_score = cursor.fetchone()['avg_score']

    # Most common category
    cursor.execute('''
        SELECT predicted_category, COUNT(*) as count
        FROM analysis_results
        GROUP BY predicted_category
        ORDER BY count DESC
        LIMIT 1
    ''')
    top_category = cursor.fetchone()

    # Score distribution
    cursor.execute('''
        SELECT
            SUM(CASE WHEN ats_score >= 75 THEN 1 ELSE 0 END) as excellent,
            SUM(CASE WHEN ats_score >= 60 AND ats_score < 75 THEN 1 ELSE 0 END) as good,
            SUM(CASE WHEN ats_score >= 45 AND ats_score < 60 THEN 1 ELSE 0 END) as moderate,
            SUM(CASE WHEN ats_score < 45 THEN 1 ELSE 0 END) as weak
        FROM analysis_results
    ''')
    distribution = cursor.fetchone()

    conn.close()

    return {
        'total'        : total,
        'avg_score'    : round(avg_score, 2) if avg_score else 0,
        'top_category' : top_category['predicted_category'] if top_category else 'N/A',
        'excellent'    : distribution['excellent'] or 0,
        'good'         : distribution['good'] or 0,
        'moderate'     : distribution['moderate'] or 0,
        'weak'         : distribution['weak'] or 0,
    }


def delete_all():
    """
    Clear all records from database.
    Used for reset functionality.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM analysis_results')
    conn.commit()
    conn.close()


# Create tables when this file is imported
create_tables()
