import streamlit as st

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# -------------------------------
# Header
# -------------------------------

st.title("📄 AI Resume Analyzer & ATS Dashboard")

st.markdown(
"""
### Welcome to AI Resume Analyzer

Analyze resumes using **Natural Language Processing (NLP)** and compare them against Job Descriptions.

This application provides:

- 📈 ATS Match Score
- 🛠 Skill Extraction
- ✅ Skill Matching
- ❌ Missing Skills
- 🤖 AI Suggestions
- 📊 Interactive Dashboard
- 🏢 Company Bulk Screening

---
"""
)

# -------------------------------
# Features
# -------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.info(
        """
### 👤 Personal Screening

Analyze a single resume against a Job Description.

✔ ATS Score

✔ Skill Matching

✔ Resume Insights

✔ Dashboard
"""
    )

with col2:

    st.success(
        """
### 🏢 Company Screening

Upload multiple resumes.

✔ Candidate Ranking

✔ Bulk ATS Screening

✔ CSV Report

✔ Shortlisting
"""
    )

with col3:

    st.warning(
        """
### 📊 Dashboard

Professional Analytics Dashboard.

✔ KPIs

✔ Charts

✔ Gauge

✔ AI Suggestions
"""
    )

st.write("---")

st.subheader("🚀 How to Use")

st.markdown("""
1. Select a page from the **left sidebar**.

2. Upload Resume(s).

3. Upload or Paste Job Description.

4. Click Analyze.

5. View Dashboard.
""")

st.write("---")

st.success(
    "Select **Personal Screening** or **Company Screening** from the left sidebar to begin."
)