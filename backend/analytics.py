from fastapi import APIRouter
from database import resumes_collection
import collections

router = APIRouter()

@router.get("/analytics")
def get_resume_analytics():
    """Generate resume statistics"""
    resumes = list(resumes_collection.find({}, {"_id": 0, "text": 1}))

    skill_counts = collections.Counter()
    total_resumes = len(resumes)

    for resume in resumes:
        words = resume["text"].split()
        skill_counts.update(words)

    # Get top 10 skills
    top_skills = skill_counts.most_common(10)

    return {
        "total_resumes": total_resumes,
        "top_skills": [{"skill": skill, "count": count} for skill, count in top_skills]
    }
