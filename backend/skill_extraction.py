import spacy

# Load pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

# Sample list of required skills (can be expanded)
REQUIRED_SKILLS = {"Python", "Machine Learning", "Deep Learning", "NLP", "Data Science", 
                   "SQL", "TensorFlow", "PyTorch", "Flask", "FastAPI", "MongoDB"}

def extract_skills(text):
    """Extracts skills from resume text"""
    doc = nlp(text)
    extracted_skills = set()

    for token in doc:
        if token.text in REQUIRED_SKILLS:
            extracted_skills.add(token.text)

    return extracted_skills

def match_skills(job_description, resume_text):
    """Compares job description skills with extracted resume skills"""
    job_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    matched_skills = job_skills.intersection(resume_skills)
    missing_skills = job_skills.difference(resume_skills)

    return {
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills)
    }
