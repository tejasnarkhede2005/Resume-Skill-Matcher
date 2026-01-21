import re
import nltk
from PyPDF2 import PdfReader
from skills import SKILLS

nltk.download('punkt')

def extract_text_from_pdf(pdf):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

def extract_skills(text):
    found = set()
    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found.add(skill)
    return found

def calculate_match(resume_skills, jd_skills):
    if not jd_skills:
        return 0
    return round((len(resume_skills & jd_skills) / len(jd_skills)) * 100, 2)
