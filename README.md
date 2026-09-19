# 🎯 Smart Resume Analyzer with AI-Based Feedback

A Flask-powered web application that analyzes resumes using NLP techniques, evaluates ATS (Applicant Tracking System) compatibility, and delivers smart, actionable feedback — all tailored to your target job role.

---

## ✨ Features

- **📄 Resume Upload & Parsing** — Supports PDF and DOCX formats (up to 10 MB)
- **📊 Resume Score Analyzer** — Evaluates structure and completeness across key sections (Education, Experience, Skills, Projects, etc.) and scores out of 100
- **🤖 ATS Keyword Checker** — Matches resume content against role-specific keyword databases for 8 career paths
- **💡 Smart Feedback System** — Generates prioritized (High / Medium / Low) actionable suggestions
- **📈 Analysis Dashboard** — Visual breakdown of scores, found/missing sections, and keyword gaps
- **🗂️ Resume History** — Persists all past analyses in a local SQLite database

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.x, Flask |
| NLP | spaCy (`en_core_web_sm`), NLTK |
| File Parsing | PyPDF2, python-docx |
| Database | SQLite (via `sqlite3`) |
| Frontend | HTML, CSS, JavaScript (Jinja2 templates) |

---

## 📁 Project Structure

```
ATS/
├── app.py              # Flask application & route definitions
├── nlp_engine.py       # NLP core: scoring, ATS analysis, feedback generation
├── file_parser.py      # Resume text extraction (PDF & DOCX)
├── database.py         # SQLite database initialization & queries
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates (index, dashboard, history, 404)
├── static/             # CSS, JS, and other static assets
└── uploads/            # Uploaded resume files (auto-created)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/Nantu-06/Smart-Resume-Analyzer-With-AI-Based-Feedback.git
cd Smart-Resume-Analyzer-With-AI-Based-Feedback
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### 4. Run the Application

```bash
python app.py
```

The app will be available at **http://127.0.0.1:5000**

---

## 🎯 Supported Job Roles

The ATS keyword checker includes curated keyword databases for the following roles:

| Role | Key Skills Checked |
|---|---|
| 🔢 Data Analyst | Python, SQL, Tableau, Pandas, Power BI... |
| 🌐 Web Developer | HTML, CSS, React, Node.js, REST API... |
| 🤖 AI Engineer | TensorFlow, PyTorch, NLP, Deep Learning... |
| 💻 Software Engineer | Algorithms, Data Structures, Docker, Agile... |
| ⚙️ DevOps Engineer | Docker, Kubernetes, CI/CD, Terraform, AWS... |
| 🔒 Cybersecurity Analyst | Pen Testing, SIEM, Incident Response... |
| 📱 Mobile Developer | React Native, Flutter, Swift, Kotlin... |
| ☁️ Cloud Engineer | AWS, Azure, GCP, Serverless, Terraform... |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Home page with upload form |
| `POST` | `/analyze` | Analyzes uploaded resume; returns JSON result |
| `GET` | `/dashboard/<record_id>` | Renders the analysis dashboard |
| `GET` | `/history` | Lists all past resume analyses |
| `GET` | `/api/record/<record_id>` | Returns raw JSON for a specific record |

---

## 🧠 How It Works

```
Resume Upload (PDF/DOCX)
        │
        ▼
  Text Extraction  (file_parser.py)
        │
        ▼
  Resume Scoring   (Module 2 — nlp_engine.py)
  • Detects sections using keyword synonyms
  • Scores each section by weighted importance
  • Detects contact info (email, phone, LinkedIn, GitHub)
        │
        ▼
  ATS Keyword Check (Module 3 — nlp_engine.py)
  • Compares resume against role-specific keyword list
  • Word-boundary-aware matching to avoid false positives
  • Returns found/missing keywords + compatibility %
        │
        ▼
  Feedback Generation (Module 4 — nlp_engine.py)
  • Prioritized suggestions (High / Medium / Low)
  • Section-level + keyword-level + score-level advice
        │
        ▼
  Results saved to SQLite → Dashboard rendered
```

---

## 📋 Requirements

```
Flask>=3.0.3
spacy>=3.8.0
nltk>=3.8.1
PyPDF2>=3.0.1
python-docx>=1.1.2
```

---

## ⚠️ Limitations

- Scanned or image-only PDFs are not supported (no OCR)
- Maximum file size is 10 MB
- Keyword matching is rule-based; it does not use semantic similarity

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built with ❤️ using Flask & spaCy
