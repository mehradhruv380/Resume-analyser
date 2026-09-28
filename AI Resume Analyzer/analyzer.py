import re


# -----------------------------------
# EMAIL
# -----------------------------------

def extract_email(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    emails = re.findall(pattern, text)

    if emails:
        return emails[0]

    return "Not Found"


# -----------------------------------
# PHONE
# -----------------------------------

def extract_phone(text):
    pattern = r'(\+91[\s-]?)?[6-9]\d{9}'

    phones = re.findall(pattern, text)

    if phones:
        return phones[0]

    return "Not Found"


# -----------------------------------
# SKILLS
# -----------------------------------

def find_skills(text):

    skills_list = [
        "python",
        "java",
        "javascript",
        "typescript",
        "c++",
        "c",
        "php",

        "html",
        "css",

        "react",
        "next.js",
        "node.js",
        "node",
        "express",

        "mongodb",
        "mysql",
        "sql",

        "git",
        "github",

        "docker",
        "aws",

        "rest api",
        "api",

        "tailwind",

        "machine learning",
        "deep learning",
        "artificial intelligence",

        "data analysis",

        "pandas",
        "numpy",

        "tensorflow",
        "pytorch",

        "laravel"
    ]

    text_lower = text.lower()

    found_skills = []

    for skill in skills_list:

        if skill in text_lower:

            found_skills.append(skill)

    return found_skills


# -----------------------------------
# KEYWORDS
# -----------------------------------

def extract_keywords(text):

    text_lower = text.lower()

    text_lower = re.sub(
        r'[^a-z0-9+#.\s]',
        ' ',
        text_lower
    )

    words = text_lower.split()

    stop_words = {
        "the", "and", "for", "with",
        "you", "your", "our", "are",
        "this", "that", "will",
        "from", "have", "has",
        "been", "being", "job",
        "role", "work", "working",
        "years", "year", "into",
        "about", "who", "what",
        "where", "when", "can",
        "should", "must", "they",
        "their", "we", "is",
        "in", "of", "to",
        "a", "an", "on",
        "as", "at", "or",
        "be", "it", "by"
    }

    keywords = []

    for word in words:

        if len(word) > 2 and word not in stop_words:

            if word not in keywords:

                keywords.append(word)

    return keywords


# -----------------------------------
# MATCHED KEYWORDS
# -----------------------------------

def find_matched_keywords(
    resume_text,
    job_description
):

    resume_lower = resume_text.lower()

    keywords = extract_keywords(
        job_description
    )

    matched = []

    for keyword in keywords:

        if keyword in resume_lower:

            matched.append(keyword)

    return matched


# -----------------------------------
# MISSING KEYWORDS
# -----------------------------------

def find_missing_keywords(
    resume_text,
    job_description
):

    resume_lower = resume_text.lower()

    keywords = extract_keywords(
        job_description
    )

    missing = []

    for keyword in keywords:

        if keyword not in resume_lower:

            missing.append(keyword)

    return missing


# -----------------------------------
# ATS SCORE
# -----------------------------------

def calculate_ats_score(
    resume_text,
    job_description
):

    keywords = extract_keywords(
        job_description
    )

    if not keywords:

        return 0

    resume_lower = resume_text.lower()

    matched = []

    for keyword in keywords:

        if keyword in resume_lower:

            matched.append(keyword)

    score = (
        len(matched) /
        len(keywords)
    ) * 100

    return round(score)


# -----------------------------------
# SECTION DETECTION
# -----------------------------------

def detect_sections(text):

    text_lower = text.lower()

    sections = {

        "Education": [
            "education",
            "academic",
            "qualification"
        ],

        "Experience": [
            "experience",
            "work experience",
            "employment"
        ],

        "Skills": [
            "skills",
            "technical skills",
            "technologies"
        ],

        "Projects": [
            "projects",
            "project"
        ],

        "Certifications": [
            "certification",
            "certifications",
            "certificate"
        ]
    }

    detected = {}

    for section, keywords in sections.items():

        found = False

        for keyword in keywords:

            if keyword in text_lower:

                found = True
                break

        detected[section] = found

    return detected


# -----------------------------------
# RESUME SCORE
# -----------------------------------

def calculate_resume_score(
    resume_text,
    result
):

    score = 0

    # Email
    if result["email"] != "Not Found":

        score += 10

    # Phone
    if result["phone"] != "Not Found":

        score += 10


    # Word count
    word_count = result["word_count"]

    if word_count >= 300:

        score += 10

    if word_count >= 500:

        score += 10


    # Skills
    skill_count = len(
        result["skills"]
    )

    if skill_count >= 5:

        score += 10

    if skill_count >= 10:

        score += 10


    # Sections
    sections = detect_sections(
        resume_text
    )

    for section, exists in sections.items():

        if exists:

            score += 5


    return min(score, 100)


# -----------------------------------
# COMPLETE ANALYSIS
# -----------------------------------

def analyze_resume(text):

    result = {

        "email": extract_email(text),

        "phone": extract_phone(text),

        "skills": find_skills(text),

        "word_count": len(text.split()),

        "sections": detect_sections(text)
    }

    return result