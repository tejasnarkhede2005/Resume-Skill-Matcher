import streamlit as st
from utils import extract_text_from_pdf, extract_skills, calculate_match

st.set_page_config(
    page_title="Resume Skill Matcher",
    layout="wide"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1>Resume Skill Matcher</h1>", unsafe_allow_html=True)
st.write("Upload your resume and compare it with a job description")

col1, col2 = st.columns(2)

with col1:
    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    jd = st.text_area("Paste Job Description", height=250)

if resume and jd:
    resume_text = extract_text_from_pdf(resume)
    jd_text = jd.lower()

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    match_percentage = calculate_match(resume_skills, jd_skills)
    missing_skills = jd_skills - resume_skills

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='match'>Match Score: {match_percentage}%</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><h3>Matched Skills</h3>", unsafe_allow_html=True)
    for skill in resume_skills & jd_skills:
        st.markdown(f"<span class='skill'>{skill}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><h3>Missing Skills</h3>", unsafe_allow_html=True)
    for skill in missing_skills:
        st.markdown(f"<span class='skill'>{skill}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
