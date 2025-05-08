# database.py
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["resume_screening"]
resumes_collection = db["resumes"]
