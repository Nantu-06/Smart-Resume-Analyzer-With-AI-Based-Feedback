import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'resume_analyzer.db')

def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            target_role TEXT NOT NULL,
            resume_score REAL NOT NULL,
            ats_score REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER NOT NULL,
            suggestion TEXT NOT NULL,
            FOREIGN KEY (resume_id) REFERENCES resumes(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS missing_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER NOT NULL,
            skill TEXT NOT NULL,
            FOREIGN KEY (resume_id) REFERENCES resumes(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS missing_sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER NOT NULL,
            section TEXT NOT NULL,
            FOREIGN KEY (resume_id) REFERENCES resumes(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")


def save_resume_data(filename, target_role, resume_score, ats_score,
                     suggestions=None, missing_skills=None, missing_sections=None):
    """Save resume analysis results to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO resumes (filename, target_role, resume_score, ats_score)
        VALUES (?, ?, ?, ?)
    ''', (filename, target_role, resume_score, ats_score))

    record_id = cursor.lastrowid

    if suggestions:
        for suggestion in suggestions:
            cursor.execute('INSERT INTO feedback (resume_id, suggestion) VALUES (?, ?)',
                           (record_id, suggestion))

    if missing_skills:
        for skill in missing_skills:
            cursor.execute('INSERT INTO missing_skills (resume_id, skill) VALUES (?, ?)',
                           (record_id, skill))

    if missing_sections:
        for section in missing_sections:
            cursor.execute('INSERT INTO missing_sections (resume_id, section) VALUES (?, ?)',
                           (record_id, section))

    conn.commit()
    conn.close()
    return record_id


def get_resume_data(record_id):
    """Fetch a full resume analysis record by ID."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM resumes WHERE id = ?', (record_id,))
    resume = cursor.fetchone()

    if not resume:
        conn.close()
        return None

    cursor.execute('SELECT suggestion FROM feedback WHERE resume_id = ?', (record_id,))
    suggestions = [row['suggestion'] for row in cursor.fetchall()]

    cursor.execute('SELECT skill FROM missing_skills WHERE resume_id = ?', (record_id,))
    skills = [row['skill'] for row in cursor.fetchall()]

    cursor.execute('SELECT section FROM missing_sections WHERE resume_id = ?', (record_id,))
    sections = [row['section'] for row in cursor.fetchall()]

    conn.close()

    return {
        "id": resume['id'],
        "filename": resume['filename'],
        "target_role": resume['target_role'],
        "resume_score": resume['resume_score'],
        "ats_score": resume['ats_score'],
        "created_at": resume['created_at'],
        "suggestions": suggestions,
        "missing_skills": skills,
        "missing_sections": sections
    }


def get_all_resumes():
    """Fetch all resume records for history listing."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resumes ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
