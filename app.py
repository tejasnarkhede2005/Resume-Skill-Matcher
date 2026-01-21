import streamlit as st
import matplotlib.pyplot as plt
from utils import extract_text_from_pdf, extract_skills, calculate_match, score_badge

st.set_page_config("Resume Skill Matcher", layout="centered")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# Navbar
st.markdown("""
<div class="navbar">
    <div class="nav-title">Resume Skill Matcher</div>
    <div class="nav-tabs">
        <button onclick="window.location.reload()">Dashboard</button>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Dashboard"):
        st.session_state.page = "Dashboard"
with col2:
    if st.button("Analysis"):
        st.session_state.page = "Analysis"
with col3:
    if st.button("About"):
        st.session_state.page = "About"

# ---------------- DASHBOARD ----------------
if st.session_state.page == "Dashboard":
    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd = st.text_area("Paste Job Description", height=180)

    if resume and jd:
        resume_text = extract_text_from_pdf(resume)
        jd_text = jd.lower()

        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)

        score = calculate_match(resume_skills, jd_skills)
        matched = resume_skills & jd_skills
        missing = jd_skills - resume_skills

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='score'>{score}%</div>", unsafe_allow_html=True)
        st.progress(score / 100)
        st.markdown(f"<div class='badge'>{score_badge(score)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h4>Matched Skills</h4>", unsafe_allow_html=True)
        for s in matched:
            st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h4>Missing Skills</h4>", unsafe_allow_html=True)
        for s in missing:
            st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ANALYSIS ----------------
elif st.session_state.page == "Analysis":
    st.markdown("<div class='card'><h3>Skill Distribution</h3></div>", unsafe_allow_html=True)

    if "resume_skills" in locals():
        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        ax.pie(
            [len(matched), len(missing)],
            labels=["Matched", "Missing"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("Upload resume and job description first.")

# ---------------- ABOUT ----------------
else:
    st.markdown("""
    <div class="card">
        <h3>About</h3>
        <p>
        Resume Skill Matcher is a mobile-app–style Streamlit application that
        compares resumes with job descriptions and calculates a skill match score.
        </p>
        <p>
        Built using Python, NLP, regex, and clean UI principles.
        </p>
    </div>
    """, unsafe_allow_html=True)
