import pdfplumber
import docx
from io import BytesIO

def extract_text_from_pdf(pdf_bytes):
    text = ""
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(file_path):
    """Extracts text from a DOCX file"""
    try:
        doc = docx.Document(file_path)
        extracted_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return extracted_text
    except Exception as e:
        print(f"Error extracting text from DOCX: {str(e)}")
        return ""
