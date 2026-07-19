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
    page_title="Company Screening",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Company Resume Screening")

st.markdown(
    """
Screen multiple resumes against a Job Description.

Upload multiple resumes and rank candidates based on ATS Score.
"""
)

st.write("---")

# ==================================================
# Upload Resumes
# ==================================================

resumes = st.file_uploader(
    "📂 Upload Resumes",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

st.write("")

job_description = st.text_area(
    "📝 Paste Job Description",
    height=170
)

st.markdown("### OR")

jd_file = st.file_uploader(
    "Upload Job Description",
    type=["pdf", "txt"]
)

st.write("")

analyze = st.button(
    "🚀 Screen All Resumes",
    use_container_width=True
)

# ==================================================
# Screening
# ==================================================

if analyze:

    if len(resumes) == 0:

        st.warning("Please upload at least one Resume.")
        st.stop()

    if job_description.strip() == "" and jd_file is None:

        st.warning("Please provide a Job Description.")
        st.stop()

    # ---------------------------
    # Read JD
    # ---------------------------

    if jd_file:

        job_text = extract_text(jd_file)

    else:

        job_text = job_description

    clean_job = clean_text(job_text)

    job_skills = extract_skills(clean_job)

    # ---------------------------
    # Progress Bar
    # ---------------------------

    progress = st.progress(0)

    results = []

    total = len(resumes)

    # ---------------------------
    # Process Each Resume
    # ---------------------------

    for index, resume in enumerate(resumes):

        resume_text = extract_text(resume)
        candidate_name = extract_name(resume_text)
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)

        clean_resume = clean_text(resume_text)

        resume_skills = extract_skills(clean_resume)

        scores = calculate_similarity(

            clean_resume,
            clean_job,
            resume_skills,
            job_skills

        )

        recommendation = get_recommendation(
            scores["final_score"],
            csv=True
        )
        matched = len(
            set(resume_skills) &
            set(job_skills)
        )

        missing = len(
            set(job_skills) -
            set(resume_skills)
        )

        results.append({

            "Candidate":
            candidate_name,

            "Email":
            email,

            "Mobile":
            phone,

            "Resume File":
            resume.name,

            "ATS Score":
            scores["final_score"],

            "TF-IDF Score":
            scores["tfidf_score"],

            "Skill Match":
            scores["skill_score"],

            "Matched Skills":
            matched,

            "Missing Skills":
            missing,

            "Recommendation":
            recommendation

        })

        progress.progress(
            (index + 1) / total
        )

    # ==================================================
    # DataFrame
    # ==================================================

    df = pd.DataFrame(results)

    df = df.sort_values(

        by="ATS Score",

        ascending=False

    ).reset_index(drop=True)

    # ==================================================
    # KPI Cards
    # ==================================================

    st.success(
        f"Successfully screened {len(df)} resumes."
    )

    st.write("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Resumes",
        len(df)
    )

    c2.metric(
        "Highest ATS",
        f"{df['ATS Score'].max():.2f}%"
    )

    c3.metric(
        "Average ATS",
        f"{df['ATS Score'].mean():.2f}%"
    )

    shortlisted = len(
        df[df["ATS Score"] >= 70]
    )

    c4.metric(
        "Shortlisted",
        shortlisted
    )

    st.write("---")


    # Data shown on Streamlit

    display_df = df.drop(
        columns=[
            "Email",
            "Mobile"
        ]
    )

    

    # ==================================================
    # Candidate Ranking
    # ==================================================

    st.subheader("🏆 Candidate Ranking")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    st.write("---")

    # ==================================================
    # Top Candidate
    # ==================================================

    st.subheader("🥇 Best Candidate")

    top = df.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Candidate",
        top["Candidate"]
    )

    col2.metric(
        "ATS Score",
        f"{top['ATS Score']}%"
    )

    col3.metric(
        "Recommendation",
        top["Recommendation"]
    )

    st.write("---")

    # ==================================================
    # Download Report
    # ==================================================


    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Screening Report",
        data=csv,
        file_name="Resume_Screening_Report.csv",
        mime="text/csv"
    )

    