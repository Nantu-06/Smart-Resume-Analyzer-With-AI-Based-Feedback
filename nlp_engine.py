import re
import spacy

# ---------------------------------------------------------------------------
# Load spaCy NLP model
# Run once: python -m spacy download en_core_web_sm
# ---------------------------------------------------------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError(
        "spaCy model 'en_core_web_sm' not found.\n"
        "Please run: python -m spacy download en_core_web_sm"
    )

# ---------------------------------------------------------------------------
# Industry Keyword Database  (Module 3)
# ---------------------------------------------------------------------------
INDUSTRY_KEYWORDS: dict[str, list[str]] = {
    "Data Analyst": [
        "python", "sql", "excel", "tableau", "statistics", "pandas",
        "numpy", "power bi", "data visualization", "machine learning",
        "r programming", "etl", "spark", "hadoop"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react", "node", "express",
        "mongodb", "rest api", "git", "typescript", "vue", "angular",
        "webpack", "docker", "sql"
    ],
    "AI Engineer": [
        "python", "machine learning", "tensorflow", "nlp", "spacy",
        "pytorch", "deep learning", "scikit-learn", "data preprocessing",
        "neural networks", "transformers", "hugging face", "cuda", "mlops"
    ],
    "Software Engineer": [
        "python", "java", "c++", "data structures", "algorithms",
        "git", "agile", "rest api", "sql", "docker", "kubernetes",
        "system design", "linux", "unit testing"
    ],
    "DevOps Engineer": [
        "docker", "kubernetes", "jenkins", "ci/cd", "linux",
        "aws", "azure", "terraform", "ansible", "git",
        "monitoring", "bash", "python", "nginx"
    ],
    "Cybersecurity Analyst": [
        "network security", "penetration testing", "siem", "firewalls",
        "incident response", "vulnerability assessment", "python",
        "linux", "cryptography", "ethical hacking", "wireshark", "nmap"
    ],
    "Mobile Developer": [
        "react native", "flutter", "swift", "kotlin", "java",
        "android", "ios", "rest api", "git", "firebase",
        "ui/ux", "typescript", "dart"
    ],
    "Cloud Engineer": [
        "aws", "azure", "gcp", "terraform", "docker",
        "kubernetes", "linux", "python", "networking",
        "ci/cd", "serverless", "iam", "s3", "ec2"
    ],
}

# Sections scoring weights (Module 2)
SECTION_WEIGHTS: dict[str, int] = {
    "education": 15,
    "experience": 25,
    "projects": 20,
    "skills": 20,
    "summary": 10,
    "certifications": 5,
    "contact": 5,
}

# Common contact patterns
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
PHONE_PATTERN = re.compile(r'(\+?\d[\d\s\-().]{7,}\d)')
LINKEDIN_PATTERN = re.compile(r'linkedin\.com', re.IGNORECASE)
GITHUB_PATTERN = re.compile(r'github\.com', re.IGNORECASE)


# ===========================================================================
# Module 2: Resume Score Analyzer
# ===========================================================================

def generate_resume_score(text: str) -> dict:
    """
    Evaluates resume structure, completeness, and quality.
    Returns a score out of 100 with a detailed breakdown.
    """
    text_lower = text.lower()
    doc = nlp(text_lower)

    score = 0
    breakdown = {}
    missing_sections = []
    found_sections = []

    # --- Section Detection ---
    for section, weight in SECTION_WEIGHTS.items():
        # Use broad synonyms for better detection
        synonyms = _get_section_synonyms(section)
        if any(syn in text_lower for syn in synonyms):
            score += weight
            breakdown[section] = weight
            found_sections.append(section)
        else:
            breakdown[section] = 0
            missing_sections.append(section)

    # --- Contact Info Bonus (5 pts) ---
    contact_score = 0
    if EMAIL_PATTERN.search(text):
        contact_score += 2
    if PHONE_PATTERN.search(text):
        contact_score += 1
    if LINKEDIN_PATTERN.search(text):
        contact_score += 1
    if GITHUB_PATTERN.search(text):
        contact_score += 1
    breakdown['contact_info'] = contact_score
    score += contact_score

    # Cap at 100
    total_score = min(score, 100)

    return {
        "total_score": total_score,
        "breakdown": breakdown,
        "missing_sections": missing_sections,
        "found_sections": found_sections,
    }


def _get_section_synonyms(section: str) -> list[str]:
    """Returns a list of synonyms/variants for each resume section."""
    synonyms_map = {
        "education": ["education", "academic", "qualification", "degree", "university", "college"],
        "experience": ["experience", "work history", "employment", "professional background",
                       "internship", "career", "job"],
        "projects": ["project", "portfolio", "work samples", "case study", "capstone"],
        "skills": ["skill", "technical proficiency", "competencies", "technologies", "tools",
                   "expertise", "stack"],
        "summary": ["summary", "objective", "profile", "about me", "introduction", "overview"],
        "certifications": ["certification", "certificate", "license", "credential", "course"],
        "contact": ["contact", "email", "phone", "linkedin", "github", "address", "@"],
    }
    return synonyms_map.get(section, [section])


# ===========================================================================
# Module 3: ATS Keyword Checker
# ===========================================================================

def analyze_ats_keywords(text: str, role: str) -> dict:
    """
    Compares resume text with industry-required keywords for the target role.
    Returns compatibility score and missing/found keywords.
    """
    target_keywords = INDUSTRY_KEYWORDS.get(role, [])
    if not target_keywords:
        return {
            "compatibility_score": 0,
            "found_keywords": [],
            "missing_keywords": [],
            "total_keywords": 0,
        }

    text_lower = text.lower()
    # Use word-boundary-aware matching to avoid false positives
    found_keywords = []
    missing_keywords = []

    for kw in target_keywords:
        pattern = re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE)
        if pattern.search(text_lower):
            found_keywords.append(kw)
        else:
            missing_keywords.append(kw)

    compatibility = (len(found_keywords) / len(target_keywords)) * 100

    return {
        "compatibility_score": round(compatibility, 2),
        "found_keywords": found_keywords,
        "missing_keywords": missing_keywords,
        "total_keywords": len(target_keywords),
    }


# ===========================================================================
# Module 4: Smart Feedback System
# ===========================================================================

def generate_feedback(score_data: dict, ats_data: dict) -> dict:
    """
    Generates prioritized, actionable improvement suggestions based on analysis.
    """
    suggestions = []
    priority_map = {}  # suggestion -> priority level (high / medium / low)

    # --- Section-based feedback ---
    section_advice = {
        "summary":        "Add a professional summary/objective at the top of your resume to create a strong first impression.",
        "experience":     "Include a dedicated Work Experience or Internship section with role titles, companies, dates, and bullet-point achievements.",
        "projects":       "Add a Projects section showcasing relevant technical work. Include tech stack used and measurable outcomes.",
        "education":      "Add your Education details (degree, institution, graduation year) to meet recruiter expectations.",
        "skills":         "Create a Skills section listing your key technical and soft skills relevant to the target role.",
        "certifications": "List any certifications, online courses, or professional credentials to stand out.",
        "contact":        "Ensure contact information (email, phone, LinkedIn, GitHub) is clearly visible at the top.",
    }

    for section in score_data.get("missing_sections", []):
        advice = section_advice.get(section)
        if advice:
            suggestions.append(advice)
            priority_map[advice] = "high" if section in ("experience", "skills", "contact") else "medium"

    # --- ATS keyword feedback ---
    for skill in ats_data.get("missing_keywords", []):
        msg = f"Add '{skill.title()}' to your Skills or Experience section to improve ATS compatibility."
        suggestions.append(msg)
        priority_map[msg] = "high"

    # --- Compatibility score feedback ---
    compat = ats_data.get("compatibility_score", 0)
    if compat < 40:
        msg = "Your resume has very low ATS compatibility. Significantly restructure it with role-specific keywords."
        suggestions.append(msg)
        priority_map[msg] = "high"
    elif compat < 70:
        msg = "Improve keyword density and alignment with the job description for better ATS pass rates."
        suggestions.append(msg)
        priority_map[msg] = "medium"
    elif compat >= 85:
        suggestions.append("Great ATS alignment! Fine-tune with quantified achievements (e.g., 'Increased efficiency by 30%').")

    # --- Overall score feedback ---
    total = score_data.get("total_score", 0)
    if total < 50:
        msg = "Your resume score is low. Focus on adding all major sections: Summary, Experience, Skills, and Education."
        suggestions.append(msg)
        priority_map[msg] = "high"
    elif total < 75:
        suggestions.append("Good foundation! Strengthen weak sections and add quantifiable results to experience bullet points.")
    else:
        suggestions.append("Solid resume structure! Polish language, use action verbs, and tailor content per job application.")

    return {
        "suggestions": suggestions,
        "priority_map": priority_map,
        "total_suggestions": len(suggestions),
    }


def get_available_roles() -> list[str]:
    """Returns a list of all roles supported by the ATS keyword checker."""
    return list(INDUSTRY_KEYWORDS.keys())
