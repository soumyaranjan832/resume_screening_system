from sentence_transformers import SentenceTransformer, util

# Load pre-trained BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

def rank_resumes(job_description, resumes):
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    resume_embeddings = [model.encode(resume["text"], convert_to_tensor=True) for resume in resumes]
    
    similarity_scores = [float(util.pytorch_cos_sim(job_embedding, emb)[0][0]) for emb in resume_embeddings]
    
    ranked_resumes = sorted(zip(resumes, similarity_scores), key=lambda x: x[1], reverse=True)
    
    return [{
        "filename": r[0]["filename"],
        "score": r[1],
        "text": r[0]["text"]  # Include extracted text for display
    } for r in ranked_resumes]
