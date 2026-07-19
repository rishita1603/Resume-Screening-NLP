import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
import numpy as np

st.set_page_config(
    page_title="Candidate Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CHECK ANALYSIS
# ==========================================================

if "match_score" not in st.session_state:

    st.warning("Please analyze a resume first.")

    st.stop()


# ==========================================================
# LOAD DATA
# ==========================================================

score = st.session_state["match_score"]

resume_skills = st.session_state["resume_skills"]

job_skills = st.session_state["job_skills"]

matching = st.session_state["matching_skills"]

missing = st.session_state["missing_skills"]

recommendation = st.session_state["recommendation"]

resume_text = st.session_state["resume_text"]


# ==========================================================
# HEADER
# ==========================================================

col1, col2 = st.columns([5,1])

with col1:

    st.title("📊 Candidate Dashboard")

with col2:

    if st.button("🏠 Home"):

        st.switch_page("app.py")


st.write("---")


# ==========================================================
# CANDIDATE DETAILS
# ==========================================================

st.subheader("👤 Candidate Summary")

experience = "Fresher"

education = "Bachelor's"

text = resume_text.lower()

if "master" in text or "mca" in text or "mba" in text:

    education = "Master's"

if "experience" in text or "intern" in text:

    experience = "Experienced"


c1, c2, c3 = st.columns(3)

c1.metric("Education", education)

c2.metric("Experience", experience)

c3.metric("Recommendation", recommendation)


st.write("---")


# ==========================================================
# KPI CARDS
# ==========================================================

st.markdown("""
<style>

div[data-testid="stMetric"]{
    background-color:#161B22;
    border:1px solid #30363D;
    padding:15px;
    border-radius:15px;
}

div[data-testid="stMetric"]:hover{
    border:1px solid #8B5CF6;
    box-shadow:0px 0px 10px rgba(139,92,246,.4);
}

</style>
""", unsafe_allow_html=True)

st.subheader("📈KPIs")

k1, k2, k3, k4 = st.columns(4)

k1.metric("ATS Score", f"{score}%")

k2.metric("Resume Skills", len(resume_skills))

k3.metric("Matched Skills", len(matching))

k4.metric("Missing Skills", len(missing))


st.write("---")


# ==========================================================
# PROGRESS BAR
# ==========================================================

st.subheader("🎯 ATS Match")

st.progress(score/100)

st.write(f"### Overall ATS Score : **{score}%**")


st.write("---")

# ==========================================================
# CHARTS
# ==========================================================

col1, col2, col3 = st.columns(3)

# ---------------------------------------------------
# ATS Gauge Chart
# ---------------------------------------------------

with col1:
    plt.style.use("dark_background")

    st.subheader("🎯 ATS Gauge")

    fig, ax = plt.subplots(figsize=(4,2.5))

    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    ax.set_xlim(-1.2,1.2)
    ax.set_ylim(0,1.2)

    ax.axis("off")

    # Background
    bg = Wedge(
        (0,0),
        1,
        0,
        180,
        width=0.30,
        color="#D5D2D7"
    )

    ax.add_patch(bg)

    # Filled Portion

    angle = (score/100)*180

    fg = Wedge(
        (0,0),
        1,
        0,
        angle,
        width=0.30,
        color="#900BE9"
    )

    ax.add_patch(fg)

    centre = Circle(
        (0,0),
        0.55,
        color="#0E1117"
    )

    ax.add_patch(centre)

    ax.text(
        0,
        0.05,
        f"{score:.1f}%",
        fontsize=28,
        ha="center",
        color = "white",
        fontweight="bold"
    )

    st.pyplot(fig)

# ---------------------------------------------------
# Skills Comparison
# ---------------------------------------------------

with col2:
    plt.style.use("dark_background")

    st.subheader("📊 Skills Comparison")

    fig, ax = plt.subplots(figsize=(4,3))

    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    categories = [

        "Resume",

        "Required",

        "Matched",

        "Missing"

    ]

    values = [

        len(resume_skills),

        len(job_skills),

        len(matching),

        len(missing)

    ]

    colors = [
    "#900BE9",   
    "#9470AC",   
    "#A38FB0",  
    "#D5D2D7"   
]

    ax.bar(
        categories,
        values,
        color=colors
    )

    ax.set_ylabel("Skills")

    st.pyplot(fig)
# ---------------------------------------------------
# Match Percentage Donut
# ---------------------------------------------------

with col3:

    plt.style.use("dark_background")

    st.subheader("🥇 Match Ratio")

    fig, ax = plt.subplots(figsize=(3.2,3.2))

    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    sizes = [len(matching), len(missing)]
    labels = ["Matched", "Missing"]
    colors = ["#B165E4", "#590B8D"]

    wedges, _ = ax.pie(
        sizes,
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.38)
    )

    total = sum(sizes)

    for i, w in enumerate(wedges):

        angle = (w.theta2 + w.theta1) / 2

        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))

        ax.annotate(
            f"{labels[i]}\n{sizes[i]/total*100:.0f}%",
            xy=(0.82*x, 0.82*y),
            xytext=(1.25*x, 1.25*y),
            ha="center",
            va="center",
            fontsize=10,
            color="white",
            arrowprops=dict(
                arrowstyle="-",
                color="white",
                lw=1.2
            )
        )

    ax.set_aspect("equal")

    st.pyplot(fig)



# ==========================================================
# TABLES
# ==========================================================

left,right = st.columns(2)

with left:

    st.subheader("✅ Matching Skills")

    st.dataframe(

        pd.DataFrame(

            {

                "Skills":[

                    skill.title()

                    for skill in matching

                ]

            }

        ),

        use_container_width=True,

        hide_index=True

    )

with right:

    st.subheader("❌ Missing Skills")

    st.dataframe(

        pd.DataFrame(

            {

                "Skills":[

                    skill.title()

                    for skill in missing

                ]

            }

        ),

        use_container_width=True,

        hide_index=True

    )


st.write("---")


# ==========================================================
# AI SUGGESTIONS
# ==========================================================

st.subheader("🤖 AI Resume Suggestions")

suggestions = []

if len(missing) > 0:

    suggestions.append(

        f"Add skills like {', '.join(missing[:5])}."

    )

if score < 60:

    suggestions.append(

        "Improve your resume summary using Job Description keywords."

    )

if "project" not in resume_text.lower():

    suggestions.append(

        "Mention academic or personal projects."

    )

if "certification" not in resume_text.lower():

    suggestions.append(

        "Add relevant certifications."

    )

if "github" not in resume_text.lower():

    suggestions.append(

        "Include your GitHub profile."

    )

if "linkedin" not in resume_text.lower():

    suggestions.append(

        "Include your LinkedIn profile."

    )

for tip in suggestions:

    st.info(tip)


st.write("---")


# ==========================================================
# FINAL VERDICT
# ==========================================================

st.subheader("⭐ Final Verdict")

if score >= 80:

    st.success(
        "Excellent Resume! High chances of clearing ATS."
    )

elif score >= 60:

    st.warning(
        "Good Resume. Minor improvements can increase ATS score."
    )

else:

    st.error(
        "Resume requires significant improvements before applying."
    )