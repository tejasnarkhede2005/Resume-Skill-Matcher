import re
from PyPDF2 import PdfReader
from skills import SKILLS

def extract_text_from_pdf(pdf):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

def extract_skills(text):
    found = set()
    for skill in SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.add(skill)
    return found

def calculate_match(resume_skills, jd_skills):
    if not jd_skills:
        return 0
    return round(len(resume_skills & jd_skills) / len(jd_skills) * 100, 2)

def score_badge(score):
    if score >= 80:
        return "Excellent Match 🟢"
    elif score >= 60:
        return "Good Match 🟡"
    else:
        return "Needs Improvement 🔴"
