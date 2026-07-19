import streamlit as st
import pandas as pd

from helper import (
    extract_text,
    clean_text,
    extract_skills,
    calculate_similarity,
    get_recommendation,
    extract_email,
    extract_phone,
    extract_name
)

st.set_page_config(
    page_title="Personal Screening",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Personal Resume Screening")

st.write(
    "Upload a Resume and compare it with a Job Description."
)

st.write("---")

# ===============================
# Upload Section
# ===============================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📂 Upload Resume")

    resume = st.file_uploader(
        "Choose Resume",
        type=["pdf", "txt"]
    )

with col2:

    st.subheader("📝 Job Description")

    jd_text = st.text_area(
        "Paste Job Description",
        height=170
    )

    st.markdown("### OR")

    jd_file = st.file_uploader(
        "Upload JD",
        type=["pdf", "txt"]
    )

st.write("")

analyze = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)

# ===============================
# Analyze
# ===============================

if analyze:

    if resume is None:

        st.warning("Please upload a Resume.")

        st.stop()

    if jd_text.strip() == "" and jd_file is None:

        st.warning("Please provide a Job Description.")

        st.stop()

    resume_text = extract_text(resume)
    candidate_name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)

    if jd_file:

        job_text = extract_text(jd_file)

    else:

        job_text = jd_text

    clean_resume = clean_text(resume_text)

    clean_job = clean_text(job_text)

    resume_skills = extract_skills(clean_resume)

    job_skills = extract_skills(clean_job)

    scores = calculate_similarity(

        clean_resume,
        clean_job,
        resume_skills,
        job_skills

    )

    recommendation = get_recommendation(
        scores["final_score"]
    )

    

    matching = sorted(
        list(
            set(resume_skills)
            &
            set(job_skills)
        )
    )

    missing = sorted(
        list(
            set(job_skills)
            -
            set(resume_skills)
        )
    )

    # ===============================
    # Save for Dashboard
    # ===============================

    st.session_state["match_score"] = scores["final_score"]

    st.session_state["resume_skills"] = resume_skills

    st.session_state["job_skills"] = job_skills

    st.session_state["matching_skills"] = matching

    st.session_state["missing_skills"] = missing

    st.session_state["recommendation"] = recommendation

    st.session_state["resume_text"] = resume_text


    # ===============================
    # ATS Score
    # ===============================

    st.subheader("📈 ATS Score")

    st.progress(scores["final_score"]/100)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "ATS Score",
        f"{scores['final_score']}%"
    )

    c2.metric(
        "TF-IDF",
        f"{scores['tfidf_score']}%"
    )

    c3.metric(
        "Skill Match",
        f"{scores['skill_score']}%"
    )

    st.success(recommendation)

    st.write("---")

    # ===============================
    # Skills Table
    # ===============================

    st.subheader("📊 Resume Skills vs Required Skills")

    rows = max(
        len(resume_skills),
        len(job_skills)
    )

    resume_list = resume_skills + [""]*(rows-len(resume_skills))

    job_list = job_skills + [""]*(rows-len(job_skills))

    df = pd.DataFrame({

        "Resume Skills":

        [i.title() for i in resume_list],

        "Required Skills":

        [i.title() for i in job_list]

    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.write("---")

    # ===============================
    # Match Table
    # ===============================

    st.subheader("📋 Matching vs Missing Skills")

    rows = max(
        len(matching),
        len(missing)
    )

    match_list = matching + [""]*(rows-len(matching))

    miss_list = missing + [""]*(rows-len(missing))

    df2 = pd.DataFrame({

        "✅ Matching Skills":

        [i.title() for i in match_list],

        "❌ Missing Skills":

        [i.title() for i in miss_list]

    })

    st.dataframe(
        df2,
        use_container_width=True,
        hide_index=True
    )

    st.write("---")

    # ===============================
    # KPI Cards
    # ===============================

    a,b,c,d = st.columns(4)

    a.metric(
        "Resume Skills",
        len(resume_skills)
    )

    b.metric(
        "Required Skills",
        len(job_skills)
    )

    c.metric(
        "Matched",
        len(matching)
    )

    d.metric(
        "Missing",
        len(missing)
    )

    st.write("")

