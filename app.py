import streamlit as st
import matplotlib.pyplot as plt
from utils import extract_text_from_pdf, extract_skills, calculate_match, score_badge

st.set_page_config("Resume Skill Matcher", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

def set_page(page):
    st.session_state.page = page

st.markdown("""
<div class="navbar">
    <div class="nav-title">Resume Skill Matcher</div>
    <div class="nav-links">
        <button onclick="window.location.reload()">Dashboard</button>
    </div>
</div>
""", unsafe_allow_html=True)

col_nav1, col_nav2, col_nav3 = st.columns([1,1,1])
with col_nav1:
    if st.button("Dashboard"):
        set_page("Dashboard")
with col_nav2:
    if st.button("Analysis"):
        set_page("Analysis")
with col_nav3:
    if st.button("About"):
        set_page("About")

# ---------------- DASHBOARD ----------------
if st.session_state.page == "Dashboard":
    col1, col2 = st.columns(2)

    with col1:
        resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    with col2:
        jd = st.text_area("Paste Job Description", height=260)

    if resume and jd:
        resume_text = extract_text_from_pdf(resume)
        jd_text = jd.lower()

        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)

        score = calculate_match(resume_skills, jd_skills)
        badge = score_badge(score)
        matched = resume_skills & jd_skills
        missing = jd_skills - resume_skills

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='score'>{score}%</div>", unsafe_allow_html=True)
        st.progress(score / 100)
        st.markdown(f"<div class='badge'>{badge}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("<div class='card'><h3>Matched Skills</h3>", unsafe_allow_html=True)
            for s in matched:
                st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("<div class='card'><h3>Missing Skills</h3>", unsafe_allow_html=True)
            for s in missing:
                st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ANALYSIS ----------------
elif st.session_state.page == "Analysis":
    st.markdown("<div class='card'><h2>Skill Match Analysis</h2></div>", unsafe_allow_html=True)

    if "resume" in st.session_state:
        pass
    else:
        st.info("Upload resume and job description first from Dashboard")

    if "resume_text" in locals():
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(
            [len(matched), len(missing)],
            labels=["Matched", "Missing"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)

# ---------------- ABOUT ----------------
elif st.session_state.page == "About":
    st.markdown("""
    <div class="card">
        <h2>About This Project</h2>
        <p>
        Resume Skill Matcher is an NLP-based Streamlit application that compares resumes
        with job descriptions and calculates a skill match score.
        </p>
        <p>
        It helps recruiters and job seekers quickly understand resume relevance
        using clean UI and real-world logic.
        </p>
    </div>
    """, unsafe_allow_html=True)
