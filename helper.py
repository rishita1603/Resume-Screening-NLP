import fitz
import re
import nltk

from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills import skills


# --------------------------------------------------
# Download NLTK Stopwords (only first time)
# --------------------------------------------------

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))


# ==================================================
# PDF TEXT EXTRACTION
# ==================================================

def extract_text_pdf(uploaded_file):

    doc = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


# ==================================================
# TXT TEXT EXTRACTION
# ==================================================

def extract_text_txt(uploaded_file):

    return uploaded_file.read().decode(
        "utf-8",
        errors="ignore"
    )


# ==================================================
# AUTO DETECT FILE TYPE
# ==================================================

def extract_text(uploaded_file):

    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_pdf(uploaded_file)

    elif filename.endswith(".docx"):
        return extract_text_docx(uploaded_file)

    elif filename.endswith(".txt"):
        return extract_text_txt(uploaded_file)

    else:
        return ""


# ==================================================
# CLEAN TEXT
# ==================================================

def clean_text(text):

    text = text.lower()

    text = re.sub(r"\d+", " ", text)

    text = re.sub(
        r"[^a-zA-Z+#.\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    words = text.split()

    words = [

        word

        for word in words

        if word not in stop_words

    ]

    return " ".join(words)


# ==================================================
# SKILL EXTRACTION
# ==================================================

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))


# ==================================================
# ATS SCORE
# ==================================================

def calculate_similarity(

    resume_text,
    job_text,
    resume_skills,
    job_skills

):

    # ---------- TF-IDF Similarity ----------

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(

        [
            resume_text,
            job_text
        ]

    )

    tfidf_score = cosine_similarity(

        vectors

    )[0][1] * 100

    # ---------- Skill Match ----------

    matched = set(

        resume_skills

    ) & set(

        job_skills

    )

    if len(job_skills) == 0:

        skill_score = 0

    else:

        skill_score = (

            len(matched)

            /

            len(job_skills)

        ) * 100

    # ---------- Final ATS Score ----------

    final_score = (

        0.70 * skill_score

        +

        0.30 * tfidf_score

    )

    return {

        "tfidf_score": round(
            tfidf_score,
            2
        ),

        "skill_score": round(
            skill_score,
            2
        ),

        "final_score": round(
            final_score,
            2
        )

    }


# ==================================================
# RECOMMENDATION
# ==================================================

def get_recommendation(score):

    if score >= 80:

        return "🟢 Strong Match"

    elif score >= 60:

        return "🟡 Moderate Match"

    else:

        return "🔴 Low Match"