import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# TEXT CLEANING
# ==========================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#.\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================
# SEMANTIC SIMILARITY
# ==========================================

def calculate_similarity(resume_text, job_description):

    resume = clean_text(resume_text)

    job = clean_text(job_description)

    if not resume or not job:
        return 0

    documents = [
        resume,
        job
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]

    return round(similarity * 100)


# ==========================================
# JOB ROLE DETECTION
# ==========================================

def recommend_job_roles(skills):

    skills = [
        skill.lower()
        for skill in skills
    ]

    roles = []

    # Full Stack
    full_stack = [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "node",
        "express",
        "mongodb"
    ]

    if sum(
        skill in skills
        for skill in full_stack
    ) >= 4:

        roles.append(
            "Full Stack Developer"
        )


    # Frontend
    frontend = [
        "html",
        "css",
        "javascript",
        "react"
    ]

    if sum(
        skill in skills
        for skill in frontend
    ) >= 3:

        roles.append(
            "Frontend Developer"
        )


    # Backend
    backend = [
        "node.js",
        "node",
        "express",
        "python",
        "java",
        "php",
        "sql",
        "mongodb"
    ]

    if sum(
        skill in skills
        for skill in backend
    ) >= 3:

        roles.append(
            "Backend Developer"
        )


    # Python
    if (
        "python" in skills
        and (
            "pandas" in skills
            or "numpy" in skills
            or "data analysis" in skills
        )
    ):

        roles.append(
            "Python / Data Analyst"
        )


    # AI / ML
    ai_skills = [
        "python",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "tensorflow",
        "pytorch"
    ]

    if sum(
        skill in skills
        for skill in ai_skills
    ) >= 2:

        roles.append(
            "AI / Machine Learning Developer"
        )


    # Database
    database = [
        "sql",
        "mysql",
        "mongodb"
    ]

    if sum(
        skill in skills
        for skill in database
    ) >= 2:

        roles.append(
            "Database Developer"
        )


    if not roles:

        roles.append(
            "Junior Software Developer"
        )


    return roles


# ==========================================
# STRENGTH ANALYSIS
# ==========================================

def generate_strengths(
    resume_text,
    result
):

    strengths = []

    text = resume_text.lower()

    skills = result["skills"]


    # Skills
    if len(skills) >= 8:

        strengths.append(
            "Strong technical skill set."
        )

    elif len(skills) >= 5:

        strengths.append(
            "Good collection of technical skills."
        )


    # Projects
    if "project" in text or "projects" in text:

        strengths.append(
            "Projects are mentioned in the resume."
        )


    # Experience
    if (
        "experience" in text
        or "internship" in text
    ):

        strengths.append(
            "Practical experience or internship "
            "experience is mentioned."
        )


    # Education
    if "education" in text:

        strengths.append(
            "Educational background is included."
        )


    # Git
    if (
        "github" in text
        or "git" in text
    ):

        strengths.append(
            "Version control knowledge is included."
        )


    # APIs
    if "api" in text:

        strengths.append(
            "API development or integration "
            "experience is mentioned."
        )


    if not strengths:

        strengths.append(
            "The resume contains basic candidate information."
        )


    return strengths


# ==========================================
# WEAKNESSES
# ==========================================

def generate_weaknesses(
    resume_text,
    result
):

    weaknesses = []

    text = resume_text.lower()

    sections = result["sections"]


    if result["email"] == "Not Found":

        weaknesses.append(
            "Professional email address is missing."
        )


    if result["phone"] == "Not Found":

        weaknesses.append(
            "Phone number is missing."
        )


    if not sections["Education"]:

        weaknesses.append(
            "Education section is missing."
        )


    if not sections["Experience"]:

        weaknesses.append(
            "Experience section is missing."
        )


    if not sections["Projects"]:

        weaknesses.append(
            "Projects section is missing."
        )


    if not sections["Certifications"]:

        weaknesses.append(
            "Certifications section is missing."
        )


    if len(result["skills"]) < 5:

        weaknesses.append(
            "The resume contains relatively few "
            "technical skills."
        )


    if len(text.split()) < 300:

        weaknesses.append(
            "The resume appears relatively short."
        )


    if not weaknesses:

        weaknesses.append(
            "No major structural weakness was detected "
            "by the rule-based analysis."
        )


    return weaknesses


# ==========================================
# SUGGESTIONS
# ==========================================

def generate_suggestions(
    resume_text,
    result,
    missing_keywords
):

    suggestions = []

    sections = result["sections"]


    if result["email"] == "Not Found":

        suggestions.append(
            "Add a professional email address "
            "at the top of the resume."
        )


    if result["phone"] == "Not Found":

        suggestions.append(
            "Add your phone number."
        )


    if not sections["Projects"]:

        suggestions.append(
            "Add 2-3 relevant projects with "
            "technologies and measurable results."
        )


    if not sections["Experience"]:

        suggestions.append(
            "Add internships, freelance work, "
            "training or relevant practical experience."
        )


    if missing_keywords:

        suggestions.append(
            "Review the missing job-description keywords "
            "and add the ones that genuinely match your skills."
        )


    suggestions.append(
        "Use action verbs such as Developed, Built, "
        "Implemented, Designed and Optimized."
    )


    suggestions.append(
        "Add measurable achievements wherever possible."
    )


    suggestions.append(
        "Keep formatting simple and ATS-friendly."
    )


    return suggestions


# ==========================================
# RESUME REWRITE SUGGESTIONS
# ==========================================

def generate_rewrite_suggestions(
    resume_text
):

    suggestions = []

    text = resume_text.lower()


    if "objective" in text:

        suggestions.append(
            "Replace a generic Objective with a concise "
            "Professional Summary focused on your skills "
            "and target role."
        )

    else:

        suggestions.append(
            "Add a 2-3 line Professional Summary "
            "at the beginning of the resume."
        )


    suggestions.append(
        "Write experience bullets using: "
        "Action + Task + Technology + Result."
    )


    suggestions.append(
        "Example: Developed a responsive React application "
        "using REST APIs and improved user interaction."
    )


    suggestions.append(
        "Keep technical skills grouped into clear categories."
    )


    suggestions.append(
        "Mention technologies used in each relevant project."
    )


    return suggestions


# ==========================================
# COMPLETE AI-LIKE ANALYSIS
# ==========================================

def generate_ai_analysis(
    resume_text,
    job_description,
    result,
    missing_keywords
):

    similarity = calculate_similarity(
        resume_text,
        job_description
    )

    strengths = generate_strengths(
        resume_text,
        result
    )

    weaknesses = generate_weaknesses(
        resume_text,
        result
    )

    suggestions = generate_suggestions(
        resume_text,
        result,
        missing_keywords
    )

    rewrite_suggestions = (
        generate_rewrite_suggestions(
            resume_text
        )
    )

    job_roles = recommend_job_roles(
        result["skills"]
    )


    # Candidate summary
    skill_count = len(result["skills"])

    summary = (
        f"The candidate has a resume containing "
        f"{skill_count} detected technical skills "
        f"and approximately "
        f"{result['word_count']} words. "
        f"The resume has a {similarity}% textual similarity "
        f"with the provided job description."
    )


    return {

        "similarity": similarity,

        "summary": summary,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "suggestions": suggestions,

        "rewrite_suggestions": rewrite_suggestions,

        "job_roles": job_roles
    }