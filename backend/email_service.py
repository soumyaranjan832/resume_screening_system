from fastapi import APIRouter, HTTPException, Form

router = APIRouter()

@router.post("/send-email")
def send_email(
    recipient_email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
):
    """Sends an email to the recipient"""
    if not recipient_email or not subject or not message:
        raise HTTPException(status_code=400, detail="All fields are required.")

    # Dummy email logic (replace with real email logic)
    print(f"Sending email to: {recipient_email}")
    print(f"Subject: {subject}")
    print(f"Message: {message}")

    return {"message": "Email sent successfully", "recipient": recipient_email}
