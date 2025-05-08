from fastapi import APIRouter, HTTPException, Query
from database import resumes_collection

router = APIRouter()

@router.get("/candidates")
def get_candidates():
    """Fetch all candidates from the database"""
    candidates = list(resumes_collection.find({}, {"_id": 0, "filename": 1, "text": 1}))
    return {"candidates": candidates}

@router.get("/shortlist")
def shortlist_candidate(filename: str = Query(..., description="Filename of the resume to check")):
    """Check if a specific resume is shortlisted"""
    candidate = resumes_collection.find_one({"filename": filename}, {"_id": 0, "filename": 1, "shortlisted": 1})
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    shortlisted_status = candidate.get("shortlisted", False)
    return {"filename": filename, "shortlisted": shortlisted_status}
