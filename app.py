import streamlit as st
import matplotlib.pyplot as plt
from utils import (
    extract_text_from_pdf, extract_skills,
    ats_score, score_badge, generate_pdf
)

st.set_page_config("Resume Skill Matcher", layout="centered")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session state
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "history" not in st.session_state:
    st.session_state.history = []

# -------- DASHBOARD --------
if st.session_state.page == "Dashboard":
    st.title("Resume Skill Matcher")

    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd = st.text_area("Paste Job Description", height=160)

    if resume and jd:
        resume_text = extract_text_from_pdf(resume)
        jd_text = jd.lower()

        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)

        score = ats_score(resume_skills, jd_skills)
        matched = resume_skills & jd_skills
        missing = jd_skills - resume_skills

        st.session_state.latest = (score, matched, missing)
        st.session_state.history.append(score)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='score'>{score}%</div>", unsafe_allow_html=True)
        st.progress(score / 100)
        st.markdown(f"<div class='badge'>{score_badge(score)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><b>Matched Skills</b><br>", unsafe_allow_html=True)
        for s in matched:
            st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><b>Missing Skills</b><br>", unsafe_allow_html=True)
        for s in missing:
            st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Download PDF Report"):
            pdf = generate_pdf(score, matched, missing)
            with open(pdf, "rb") as f:
                st.download_button("Download", f, file_name=pdf)

# -------- ANALYSIS --------
elif st.session_state.page == "Analysis":
    st.title("Analysis")

    if "latest" in st.session_state:
        score, matched, missing = st.session_state.latest

        fig, ax = plt.subplots(figsize=(3.8, 3.8))
        ax.pie(
            [len(matched), len(missing)],
            labels=["Matched", "Missing"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("Upload resume first.")

# -------- HISTORY --------
elif st.session_state.page == "History":
    st.title("Score History")

    if st.session_state.history:
        for i, s in enumerate(st.session_state.history, 1):
            st.markdown(f"Attempt {i}: **{s}%**")
    else:
        st.info("No history yet.")

# -------- ABOUT --------
else:
    st.title("About")

    st.markdown("""
    Resume Skill Matcher is an ATS-style resume analysis tool designed to
    evaluate how well a resume aligns with a job description.

    It uses weighted keyword matching to prioritize core technical skills,
    simulating how real Applicant Tracking Systems score resumes.

    This project demonstrates practical NLP, clean UI design,
    and real-world problem solving for recruiters and job seekers.
    """)

# -------- BOTTOM NAV --------
st.markdown("""
<div class="bottom-nav">
    <form action="" method="post">
        <button onclick="window.location.reload()">Dashboard</button>
    </form>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("Dashboard"):
        st.session_state.page = "Dashboard"
with c2:
    if st.button("Analysis"):
        st.session_state.page = "Analysis"
with c3:
    if st.button("History"):
        st.session_state.page = "History"
with c4:
    if st.button("About"):
        st.session_state.page = "About"
