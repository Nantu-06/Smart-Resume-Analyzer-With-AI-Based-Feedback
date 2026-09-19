import os
from flask import Flask, request, render_template, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

from file_parser import extract_text
from nlp_engine import (
    generate_resume_score,
    analyze_ats_keywords,
    generate_feedback,
    get_available_roles,
)
from database import save_resume_data, init_db, get_resume_data, get_all_resumes

# ---------------------------------------------------------------------------
# App Configuration
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename: str) -> bool:
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    """Renders the main upload interface."""
    roles = get_available_roles()
    return render_template('index.html', roles=roles)


@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Full Module 1–5 Execution Pipeline:
    1. Upload & Parse → 2. Score → 3. ATS Check → 4. Feedback → 5. Dashboard
    """
    # --- Validate file ---
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files['resume']
    target_role = request.form.get('role', 'Web Developer')

    if not file or file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Please upload a PDF or DOCX file."}), 400

    # --- Module 1: Resume Upload & Parsing ---
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    resume_text = extract_text(filepath)

    if not resume_text or len(resume_text.strip()) < 50:
        return jsonify({"error": "Could not extract sufficient text from the document. "
                                 "Ensure the file is not scanned/image-only."}), 500

    # --- Module 2: Resume Score Analyzer ---
    score_data = generate_resume_score(resume_text)

    # --- Module 3: ATS Keyword Checker ---
    ats_data = analyze_ats_keywords(resume_text, target_role)

    # --- Module 4: Smart Feedback System ---
    feedback_data = generate_feedback(score_data, ats_data)

    # --- Database: Persist results ---
    record_id = save_resume_data(
        filename=filename,
        target_role=target_role,
        resume_score=score_data['total_score'],
        ats_score=ats_data['compatibility_score'],
        suggestions=feedback_data['suggestions'],
        missing_skills=ats_data['missing_keywords'],
        missing_sections=score_data['missing_sections'],
    )

    # --- Module 5: Return data for Dashboard ---
    return jsonify({
        "status": "success",
        "record_id": record_id,
        "redirect_url": url_for('dashboard', record_id=record_id),
        "dashboard_data": {
            "filename": filename,
            "target_role": target_role,
            "resume_score": score_data['total_score'],
            "ats_compatibility_score": ats_data['compatibility_score'],
            "score_breakdown": score_data['breakdown'],
            "found_sections": score_data['found_sections'],
            "missing_sections": score_data['missing_sections'],
            "found_keywords": ats_data['found_keywords'],
            "missing_skills": ats_data['missing_keywords'],
            "total_keywords": ats_data['total_keywords'],
            "improvement_suggestions": feedback_data['suggestions'],
            "priority_map": feedback_data['priority_map'],
        },
    })


@app.route('/dashboard/<int:record_id>')
def dashboard(record_id: int):
    """Renders the analysis dashboard for a specific resume record."""
    data = get_resume_data(record_id)
    if not data:
        return render_template('404.html'), 404
    return render_template('dashboard.html', data=data)


@app.route('/history')
def history():
    """Shows the history of all analyzed resumes."""
    resumes = get_all_resumes()
    return render_template('history.html', resumes=resumes)


@app.route('/api/record/<int:record_id>')
def api_record(record_id: int):
    """API endpoint to fetch a resume record as JSON."""
    data = get_resume_data(record_id)
    if not data:
        return jsonify({"error": "Record not found."}), 404
    return jsonify(data)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
