from fastapi import APIRouter, UploadFile, File, HTTPException,Query
from database import resumes_collection
from ranking_model import rank_resumes
from extract_text import extract_text_from_pdf, extract_text_from_docx
from skill_extraction import match_skills
from resume_validation import validate_resume_format
import os,shutil

router = APIRouter()

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)  

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Uploads a resume file and extracts text"""
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text from DOCX or PDF
        extracted_text = ""
        if file.filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file_path)  # Function to extract text from PDFs
        elif file.filename.endswith(".docx"):
            extracted_text = extract_text_from_docx(file_path)  # Function to extract text from DOCX

        print(f"Extracted Text from {file.filename}:")
        print(extracted_text[:500])  # Print first 500 characters for debugging

        if not extracted_text:
            raise HTTPException(status_code=500, detail="Failed to extract text from file.")

        resumes_collection.insert_one({"filename": file.filename, "text": extracted_text})

        return {"message": "Resume uploaded and processed successfully.", "extracted_text": extracted_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/rank")
def get_ranked_resumes(job_description: str = Query(..., description="Job description for ranking")):
    """Ranks resumes based on job description"""
    resumes = list(resumes_collection.find({}, {"_id": 0, "filename": 1, "text": 1}))

    if not resumes:
        return {"ranked_resumes": []}

    ranked_resumes = rank_resumes(job_description, resumes)

    return {"ranked_resumes": ranked_resumes}



@router.get("/match-skills")
def get_skill_match(job_description: str = Query(..., description="Job description for skill matching")):
    """Compares job description skills with extracted resume skills"""
    resumes = list(resumes_collection.find({}, {"_id": 0, "filename": 1, "text": 1}))

    results = []
    for resume in resumes:
        skill_match = match_skills(job_description, resume["text"])
        results.append({
            "filename": resume["filename"],
            "matched_skills": skill_match["matched_skills"],
            "missing_skills": skill_match["missing_skills"]
        })

    return {"skill_match_results": results}


@router.get("/validate")
def validate_resume_endpoint(filename: str = Query(..., description="Filename of the resume to validate")):
    """Validates the formatting and structure of a resume"""
    resume = resumes_collection.find_one({"filename": filename}, {"_id": 0, "text": 1})

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    validation_result = validate_resume_format(resume["text"])
    return {"filename": filename, "validation_result": validation_result}