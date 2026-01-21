import streamlit as st
import matplotlib.pyplot as plt
from utils import extract_text_from_pdf, extract_skills, calculate_match, score_badge

st.set_page_config("Resume Skill Matcher", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="navbar">
    <div class="nav-title">Resume Skill Matcher</div>
    <div class="nav-links">
        <span>Dashboard</span>
        <span>Analysis</span>
        <span>About</span>
    </div>
</div>
""", unsafe_allow_html=True)

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
    missing = jd_skills - resume_skills

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='match-score'>{score}%</div>", unsafe_allow_html=True)
    st.progress(score / 100)
    st.markdown(f"<div class='badge'>{badge}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='card'><h3>Matched Skills</h3>", unsafe_allow_html=True)
        for s in resume_skills & jd_skills:
            st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("<div class='card'><h3>Missing Skills</h3>", unsafe_allow_html=True)
        for s in missing:
            st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Chart
    labels = ["Matched", "Missing"]
    values = [len(resume_skills & jd_skills), len(missing)]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)
