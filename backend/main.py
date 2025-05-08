from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from candidate_dashboard import router as candidate_router
from email_service import router as email_router

app = FastAPI()
app.include_router(router)
app.include_router(candidate_router) 
app.include_router(email_router) 
from fastapi import FastAPI
from routes import router as main_router
from candidate_dashboard import router as candidate_router
from email_service import router as email_router
from analytics import router as analytics_router

app = FastAPI()

# Include different routers
app.include_router(main_router)  # Main routes
app.include_router(candidate_router)  # Candidate Dashboard routes
app.include_router(email_router)  # Email Service routes
app.include_router(analytics_router)  # Analytics routes

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Resume Screening API"}

# ✅ Ensure this line is present

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
