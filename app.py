import streamlit as st
import pandas as pd

from helper import extract_text,clean_text,extract_skills,calculate_similarity,get_recommendation


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Resume Screening using NLP",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Screening using NLP")
st.markdown(
    "Analyze resumes against a Job Description using NLP and ATS Scoring"
)

st.write("---")

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("📄 Resume Screening")

mode = st.sidebar.radio(
    "Choose Screening Mode",
    [
        "👤 Personal Screening",
        "🏢 Company Screening"
    ]
)

st.sidebar.write("---")

# ---------------------------------------------------
# Function to Display Analysis
# ---------------------------------------------------

def display_results(
    resume_skills,
    job_skills,
    scores
):

    matching_skills = sorted(
        list(set(resume_skills) & set(job_skills))
    )

    missing_skills = sorted(
        list(set(job_skills) - set(resume_skills))
    )

    recommendation = get_recommendation(
        scores["final_score"]
    )

    # -------------------------------------

    st.subheader("📈 ATS Match Score")

    st.progress(
        scores["final_score"] / 100
    )

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

    # -------------------------------------
    # Resume Skills Table
    # -------------------------------------

    st.subheader("📊 Resume Skills vs Required Skills")

    max_len = max(
        len(resume_skills),
        len(job_skills)
    )

    resume_list = resume_skills + [
        ""
    ] * (
        max_len - len(resume_skills)
    )

    job_list = job_skills + [
        ""
    ] * (
        max_len - len(job_skills)
    )

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

    st.write("")

    # -------------------------------------
    # Matching Table
    # -------------------------------------

    st.subheader("📋 Matching vs Missing Skills")

    max_len = max(
        len(matching_skills),
        len(missing_skills)
    )

    match_list = matching_skills + [
        ""
    ] * (
        max_len - len(matching_skills)
    )

    miss_list = missing_skills + [
        ""
    ] * (
        max_len - len(missing_skills)
    )

    df = pd.DataFrame({

        "✅ Matching Skills":
        [i.title() for i in match_list],

        "❌ Missing Skills":
        [i.title() for i in miss_list]

    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.write("---")

    a, b, c, d = st.columns(4)

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
        len(matching_skills)
    )

    d.metric(
        "Missing",
        len(missing_skills)
    )

# ===================================================
# PERSONAL SCREENING
# ===================================================

if mode == "👤 Personal Screening":

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📂 Upload Resume")

        resume = st.file_uploader(
            "Choose Resume",
            type=[
                "pdf",
                "docx",
                "txt"
            ],
            key="resume_personal"
        )

    with col2:

        st.subheader("📝 Job Description")

        job_description = st.text_area(
            "Paste Job Description",
            height=170
        )

        st.markdown("**OR**")

        jd_file = st.file_uploader(
            "Upload Job Description",
            type=[
                "pdf",
                "docx",
                "txt"
            ],
            key="jd_personal"
        )

    analyze = st.button(
        "🚀 Analyze Resume"
    )

    if analyze:

        if resume is None:

            st.warning(
                "Please upload a resume."
            )

        elif (
            job_description.strip() == ""
            and
            jd_file is None
        ):

            st.warning(
                "Please provide a Job Description."
            )

        else:

            resume_text = extract_text(
                resume
            )

            if jd_file:

                job_text = extract_text(
                    jd_file
                )

            else:

                job_text = job_description

            clean_resume = clean_text(
                resume_text
            )

            clean_job = clean_text(
                job_text
            )

            resume_skills = extract_skills(
                clean_resume
            )

            job_skills = extract_skills(
                clean_job
            )

            scores = calculate_similarity(

                clean_resume,

                clean_job,

                resume_skills,

                job_skills

            )

            display_results(

                resume_skills,

                job_skills,

                scores

            )

            # ===================================================
# COMPANY SCREENING
# ===================================================

elif mode == "🏢 Company Screening":

    st.subheader("🏢 Bulk Resume Screening")

    st.write("Upload multiple resumes and one Job Description.")

    st.write("")

    resumes = st.file_uploader(
        "Upload Resumes",
        type=[
            "pdf",
            "docx",
            "txt"
        ],
        accept_multiple_files=True,
        key="company_resumes"
    )

    st.write("")

    job_description = st.text_area(
        "Paste Job Description",
        height=170,
        key="company_jd"
    )

    st.markdown("**OR**")

    jd_file = st.file_uploader(
        "Upload Job Description",
        type=[
            "pdf",
            "docx",
            "txt"
        ],
        key="company_jd_file"
    )

    analyze = st.button(
        "🚀 Screen All Resumes"
    )

    if analyze:

        if len(resumes) == 0:

            st.warning(
                "Please upload resumes."
            )

        elif (
            job_description.strip() == ""
            and
            jd_file is None
        ):

            st.warning(
                "Please provide a Job Description."
            )

        else:

            # ----------------------------------------

            if jd_file:

                job_text = extract_text(
                    jd_file
                )

            else:

                job_text = job_description

            clean_job = clean_text(
                job_text
            )

            job_skills = extract_skills(
                clean_job
            )

            results = []

            progress = st.progress(0)

            total = len(resumes)

            # ----------------------------------------

            for index, resume in enumerate(resumes):

                resume_text = extract_text(
                    resume
                )

                clean_resume = clean_text(
                    resume_text
                )

                resume_skills = extract_skills(
                    clean_resume
                )

                scores = calculate_similarity(

                    clean_resume,

                    clean_job,

                    resume_skills,

                    job_skills

                )

                recommendation = get_recommendation(
                    scores["final_score"]
                )

                matched = len(
                    set(resume_skills)
                    &
                    set(job_skills)
                )

                missing = len(
                    set(job_skills)
                    -
                    set(resume_skills)
                )

                results.append({

                    "Candidate":
                    resume.name,

                    "ATS Score":
                    scores["final_score"],

                    "TF-IDF":
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

            # ----------------------------------------

            results_df = pd.DataFrame(
                results
            )

            results_df = results_df.sort_values(

                by="ATS Score",

                ascending=False

            ).reset_index(
                drop=True
            )

            st.success(
                f"Successfully screened {len(results_df)} resumes."
            )

            st.write("---")

            st.subheader(
                "🏆 Candidate Ranking"
            )

            st.dataframe(

                results_df,

                use_container_width=True,

                hide_index=True

            )

            st.write("---")

            # Dashboard Metrics

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Total Resumes",
                len(results_df)
            )

            c2.metric(
                "Highest ATS",
                f"{results_df['ATS Score'].max():.2f}%"
            )

            c3.metric(
                "Average ATS",
                f"{results_df['ATS Score'].mean():.2f}%"
            )

            shortlisted = len(

                results_df[
                    results_df["ATS Score"] >= 70
                ]

            )

            c4.metric(
                "Shortlisted",
                shortlisted
            )

            st.write("---")

            csv = results_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(

                label="📥 Download Screening Report",

                data=csv,

                file_name="Resume_Screening_Report.csv",

                mime="text/csv"

            )