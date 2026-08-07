from fastapi import FastAPI, UploadFile, File
import shutil
import os

from app.services.pdf_reader import extract_text
from app.services.intent_detector import detect_intent

app = FastAPI(
    title="Semantic Validation Framework API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Semantic Validation Framework Backend Running"
    }

@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }

@app.get("/version")
def version():
    return {
        "version": "1.0.0"
    }

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from PDF
    text = extract_text(file_path)

    # Detect intent
    intent = detect_intent(text)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "intent": intent,
        "text": text
    }