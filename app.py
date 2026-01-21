import streamlit as st
import matplotlib.pyplot as plt
from utils import extract_text_from_pdf, extract_skills, calculate_match, score_badge

st.set_page_config("Resume Skill Matcher", layout="centered")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session State Init
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# Navbar
st.markdown("""
<div class="navbar">
    <div class="nav-title">Resume Skill Matcher</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Dashboard"):
        st.session_state.page = "Dashboard"
with c2:
    if st.button("Analysis"):
        st.session_state.page = "Analysis"
with c3:
    if st.button("About"):
        st.session_state.page = "About"

# ---------------- DASHBOARD ----------------
if st.session_state.page == "Dashboard":
    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd = st.text_area("Paste Job Description", height=170)

    if resume and jd:
        resume_text = extract_text_from_pdf(resume)
        jd_text = jd.lower()

        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)

        st.session_state.matched = resume_skills & jd_skills
        st.session_state.missing = jd_skills - resume_skills
        st.session_state.score = calculate_match(resume_skills, jd_skills)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='score'>{st.session_state.score}%</div>", unsafe_allow_html=True)
        st.progress(st.session_state.score / 100)
        st.markdown(f"<div class='badge'>{score_badge(st.session_state.score)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h4>Matched Skills</h4>", unsafe_allow_html=True)
        for s in st.session_state.matched:
            st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h4>Missing Skills</h4>", unsafe_allow_html=True)
        for s in st.session_state.missing:
            st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ANALYSIS ----------------
elif st.session_state.page == "Analysis":
    if "matched" not in st.session_state:
        st.info("Upload resume and job description first.")
    else:
        st.markdown("<div class='card'><h3>Skill Match Distribution</h3></div>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(3.8, 3.8))
        ax.pie(
            [len(st.session_state.matched), len(st.session_state.missing)],
            labels=["Matched", "Missing"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)

# ---------------- ABOUT ----------------
else:
    st.markdown("""
    <div class="card">
        <h3>About This Application</h3>
        <p>
        Resume Skill Matcher is a recruiter-focused NLP application designed to
        evaluate how well a resume aligns with a job description.
        </p>
        <p>
        The system extracts text from resumes, identifies technical skills using
        regex-based NLP techniques, and calculates a match score based on overlap
        with job requirements.
        </p>
        <p>
        This project demonstrates real-world problem solving, clean UI design,
        and practical NLP implementation suitable for ATS-style screening tools.
        </p>
        <p>
        Built with Python and Streamlit using a mobile-app–inspired interface.
        </p>
    </div>
    """, unsafe_allow_html=True)
