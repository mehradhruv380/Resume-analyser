import streamlit as st

from ai_analyzer import generate_ai_analysis

from resume_parser import extract_text_from_pdf

from analyzer import (
    analyze_resume,
    find_matched_keywords,
    find_missing_keywords,
    calculate_ats_score,
    calculate_resume_score
)


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# =====================================
# TITLE
# =====================================

st.title("📄 AI Resume Analyzer")

st.write(
    "Analyze your resume against a job description "
    "and identify areas for improvement."
)


# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("📌 Resume Analyzer")

st.sidebar.write(
    """
    This tool analyzes:

    ✅ Resume information

    ✅ Skills

    ✅ Job keywords

    ✅ ATS score

    ✅ Resume sections

    ✅ Missing keywords

    ✅ Improvement suggestions

    🤖 AI-powered analysis

    💪 Strengths

    ⚠️ Weaknesses

    ✍️ Resume rewriting

    💼 Job role recommendations
    """
)


# =====================================
# UPLOAD RESUME
# =====================================

st.subheader("📤 Upload Resume")

uploaded_file = st.file_uploader(
    "Upload your resume PDF",
    type=["pdf"]
)


# =====================================
# JOB DESCRIPTION
# =====================================

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here",

    height=250,

    placeholder="""
Example:

We are looking for a Full Stack Developer.

Requirements:

HTML
CSS
JavaScript
React
Node.js
Express
MongoDB
REST API
Git
SQL
Problem solving
Communication skills
"""
)


# =====================================
# ANALYZE BUTTON
# =====================================

if uploaded_file is not None:

    if st.button("🔍 Analyze Resume"):

        # ---------------------------------
        # PDF TEXT
        # ---------------------------------

        text = extract_text_from_pdf(
            uploaded_file
        )

        if not text.strip():

            st.error(
                "Unable to extract text from PDF."
            )

            st.stop()


        # ---------------------------------
        # RESUME ANALYSIS
        # ---------------------------------

        result = analyze_resume(
            text
        )


        # ---------------------------------
        # JOB ANALYSIS
        # ---------------------------------

        if job_description.strip():

            matched_keywords = (
                find_matched_keywords(
                    text,
                    job_description
                )
            )

            missing_keywords = (
                find_missing_keywords(
                    text,
                    job_description
                )
            )

            ats_score = calculate_ats_score(
                text,
                job_description
            )

        else:

            matched_keywords = []

            missing_keywords = []

            ats_score = 0


        # ---------------------------------
        # RESUME SCORE
        # ---------------------------------

        resume_score = calculate_resume_score(
            text,
            result
        )


        # ---------------------------------
        # AI ANALYSIS
        # ---------------------------------

        ai_analysis = generate_ai_analysis(
            text,
            job_description,
            result,
            missing_keywords
        )


        # =================================
        # DASHBOARD
        # =================================

        st.success(
            "Resume analyzed successfully! 🎉"
        )

        st.divider()

        st.header("📊 Resume Score Dashboard")


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "ATS Score",
                f"{ats_score}%"
            )


        with col2:

            st.metric(
                "Resume Score",
                f"{resume_score}/100"
            )


        with col3:

            st.metric(
                "Matched Keywords",
                len(matched_keywords)
            )


        with col4:

            st.metric(
                "Missing Keywords",
                len(missing_keywords)
            )


        # =================================
        # ATS PROGRESS
        # =================================

        st.subheader("🎯 ATS Score")

        st.progress(
            ats_score / 100
        )


        if ats_score >= 80:

            st.success(
                "High keyword match."
            )

        elif ats_score >= 60:

            st.warning(
                "Moderate keyword match."
            )

        else:

            st.error(
                "Low keyword match."
            )


        # =================================
        # MATCHED KEYWORDS
        # =================================

        st.subheader(
            "✅ Matched Keywords"
        )


        if matched_keywords:

            for keyword in matched_keywords:

                st.write(
                    f"🟢 {keyword}"
                )

        else:

            st.info(
                "No matched keywords."
            )


        # =================================
        # MISSING KEYWORDS
        # =================================

        st.subheader(
            "❌ Missing Keywords"
        )


        if missing_keywords:

            for keyword in missing_keywords:

                st.write(
                    f"🔴 {keyword}"
                )

        else:

            st.success(
                "No missing keywords found."
            )


        # =================================
        # CONTACT INFORMATION
        # =================================

        st.divider()

        st.header(
            "👤 Contact Information"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                "**Email:**",
                result["email"]
            )


        with col2:

            st.write(
                "**Phone:**",
                result["phone"]
            )


        # =================================
        # SKILLS
        # =================================

        st.header("💻 Skills")


        if result["skills"]:

            for skill in result["skills"]:

                st.write(
                    f"✅ {skill}"
                )

        else:

            st.warning(
                "No technical skills detected."
            )


        # =================================
        # RESUME SECTIONS
        # =================================

        st.header(
            "📑 Resume Sections"
        )


        sections = result["sections"]


        for section, exists in sections.items():

            if exists:

                st.success(
                    f"✅ {section} section found"
                )

            else:

                st.error(
                    f"❌ {section} section missing"
                )


        # =================================
        # IMPROVEMENTS
        # =================================

        st.header(
            "💡 Improvement Suggestions"
        )


        suggestions = []


        if result["email"] == "Not Found":

            suggestions.append(
                "Add a professional email address."
            )


        if result["phone"] == "Not Found":

            suggestions.append(
                "Add your phone number."
            )


        if len(result["skills"]) < 5:

            suggestions.append(
                "Add more relevant technical skills."
            )


        if not sections["Education"]:

            suggestions.append(
                "Add an Education section."
            )


        if not sections["Experience"]:

            suggestions.append(
                "Add your Experience section."
            )


        if not sections["Projects"]:

            suggestions.append(
                "Add relevant projects."
            )


        if missing_keywords:

            suggestions.append(
                "Add missing job-related keywords "
                "if you genuinely have those skills."
            )


        if result["word_count"] < 300:

            suggestions.append(
                "Your resume appears short. "
                "Consider adding relevant achievements, "
                "projects and experience."
            )


        if suggestions:

            for suggestion in suggestions:

                st.write(
                    f"🔸 {suggestion}"
                )

        else:

            st.success(
                "Your resume contains the major sections "
                "and information being checked."
            )


        # =================================
        # RESUME STATISTICS
        # =================================

        st.divider()

        st.header(
            "📈 Resume Statistics"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Word Count",
                result["word_count"]
            )


        with col2:

            st.metric(
                "Skills Detected",
                len(result["skills"])
            )


        # =================================
        # AI-POWERED ANALYSIS
        # =================================

        st.divider()

        st.header(
            "🤖 AI-Powered Resume Analysis"
        )


        # ---------------------------------
        # CANDIDATE SUMMARY
        # ---------------------------------

        st.subheader(
            "👤 Candidate Summary"
        )

        st.info(
            ai_analysis["summary"]
        )


        # ---------------------------------
        # SEMANTIC SIMILARITY
        # ---------------------------------

        if job_description.strip():

            st.subheader(
                "🧠 Job Description Similarity"
            )

            similarity = ai_analysis["similarity"]

            st.metric(
                "Semantic Similarity",
                f"{similarity}%"
            )

            st.progress(
                similarity / 100
            )


        # ---------------------------------
        # STRENGTHS
        # ---------------------------------

        st.subheader(
            "💪 Strengths"
        )

        for strength in ai_analysis["strengths"]:

            st.success(
                f"✅ {strength}"
            )


        # ---------------------------------
        # WEAKNESSES
        # ---------------------------------

        st.subheader(
            "⚠️ Areas to Improve"
        )

        for weakness in ai_analysis["weaknesses"]:

            st.warning(
                f"🔸 {weakness}"
            )


        # ---------------------------------
        # AI SUGGESTIONS
        # ---------------------------------

        st.subheader(
            "💡 AI Suggestions"
        )

        for suggestion in ai_analysis["suggestions"]:

            st.write(
                f"👉 {suggestion}"
            )


        # ---------------------------------
        # RESUME REWRITE
        # ---------------------------------

        st.subheader(
            "✍️ Resume Rewriting Suggestions"
        )

        for suggestion in ai_analysis[
            "rewrite_suggestions"
        ]:

            st.write(
                f"📝 {suggestion}"
            )


        # ---------------------------------
        # JOB ROLE RECOMMENDATION
        # ---------------------------------

        st.subheader(
            "💼 Suitable Job Roles"
        )

        for role in ai_analysis["job_roles"]:

            st.write(
                f"🎯 {role}"
            )


        # =================================
        # RESUME TEXT
        # =================================

        st.divider()

        st.header(
            "📄 Extracted Resume Text"
        )


        with st.expander(
            "View extracted text"
        ):

            st.write(text)