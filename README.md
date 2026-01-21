# Resume Skill Matcher 🚀

I handled ATS keyword weighting using a dictionary-based scoring system and added defensive checks to ensure stability during deployment and refactoring.
A professional NLP-powered Streamlit application that analyzes a resume against a job description and calculates a skill match score.  
Designed for recruiters and job seekers to quickly evaluate resume relevance.

Live Link : https://resume-skill-matcher-by-tejas.streamlit.app/
---
## 🏗 Architecture Flow (Mermaid Diagram)

```mermaid
graph TD
    A[User] --> B[Streamlit UI]

    B --> C[Upload Resume PDF]
    B --> D[Enter Job Description]

    C --> E[PDF Text Extraction]
    D --> F[Job Description Text]

    E --> G[Skill Extraction Engine]
    F --> G

    G --> H[Regex + NLP Matching]

    H --> I[Matched Skills]
    H --> J[Missing Skills]

    I --> K[Skill Match Percentage]
    J --> K

    K --> L[Progress Bar]
    K --> M[Pie Chart]
    K --> N[Resume Scoring Badge]

    L --> O[Dashboard View]
    M --> P[Analysis View]
    N --> O
```


## 🔍 What This Project Does

- Upload a resume in PDF format  
- Paste a job description  
- Extract skills using NLP + regex  
- Calculate skill match percentage  
- Suggest missing skills  
- Display progress bar, pie chart, and scoring badge  
- Navigate through Dashboard, Analysis, and About sections  

---

## 🧠 Why This Project Stands Out

- Solves a real recruiter problem  
- Demonstrates practical NLP thinking  
- Clean and professional UI with animations  
- Easy to explain and demo in interviews  
- Deployed as a live web app  

---

