import re
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
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
    for skill in SKILLS.keys():
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.add(skill)
    return found

def ats_score(resume_skills, jd_skills):
    total_weight = sum(SKILLS[s] for s in jd_skills)
    matched_weight = sum(SKILLS[s] for s in resume_skills & jd_skills)
    if total_weight == 0:
        return 0
    return round((matched_weight / total_weight) * 100, 2)

def score_badge(score):
    if score >= 80:
        return "Excellent Match 🟢"
    elif score >= 60:
        return "Good Match 🟡"
    else:
        return "Needs Improvement 🔴"

def generate_pdf(score, matched, missing):
    file_name = "resume_analysis_report.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Resume Skill Match Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Match Score: {score}%")

    y = height - 130
    c.drawString(50, y, "Matched Skills:")
    y -= 20
    for s in matched:
        c.drawString(70, y, f"- {s}")
        y -= 15

    y -= 10
    c.drawString(50, y, "Missing Skills:")
    y -= 20
    for s in missing:
        c.drawString(70, y, f"- {s}")
        y -= 15

    c.save()
    return file_name
