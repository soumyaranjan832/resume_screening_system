import re

def validate_resume_format(resume_text: str):
    """Validates the formatting and structure of a resume."""

    print("Validating Extracted Resume Text:")
    print(resume_text[:500])  # Print first 500 characters for debugging

    validation_result = {
        "valid": True,
        "issues": []
    }

    # Check if resume has a name
    if not re.search(r'(?i)\b(name|full name)\b[:\-\\s]?\w+', resume_text):
        validation_result["valid"] = False
        validation_result["issues"].append("Missing candidate name.")

    # Check if resume has contact details
    if not re.search(r'(?i)(phone|contact|mobile)\b[:\-\\s]?\d{7,}', resume_text) and \
       not re.search(r'(?i)(email)\b[:\-\\s]?[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text):
        validation_result["valid"] = False
        validation_result["issues"].append("Missing contact details.")

    # Check if resume has education details
    if not re.search(r'(?i)(education|degree|university|college|bachelor|master|phd)\b', resume_text):
        validation_result["valid"] = False
        validation_result["issues"].append("Missing education details.")

    # Check if resume has skills
    if not re.search(r'(?i)(skills|technologies|expertise)\b', resume_text):
        validation_result["valid"] = False
        validation_result["issues"].append("Missing skills section.")

    # Check if resume has work experience
    if not re.search(r'(?i)(experience|employment|work history)\b', resume_text):
        validation_result["valid"] = False
        validation_result["issues"].append("Missing work experience.")

    return validation_result
