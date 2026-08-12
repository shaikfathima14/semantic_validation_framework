from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from app.services.pdf_reader import extract_text
from app.services.intent_detector import detect_intent
from app.services.nlp import extract_entities
from app.services.validator import validate_document

app = FastAPI(
    title="Semantic Validation Framework API",
    version="1.0.0"
)

# -------------------------------
# CORS Configuration
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Upload Configuration
# -------------------------------

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------------
# Basic API Endpoints
# -------------------------------

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


# -------------------------------
# Document Upload + Validation
# -------------------------------

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    # Save uploaded document
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # -------------------------------
    # 1. Extract document text
    # -------------------------------

    text = extract_text(file_path)

    # -------------------------------
    # 2. Detect document/application type
    # -------------------------------

    intent = detect_intent(text)

    # -------------------------------
    # 3. Extract NLP entities
    # -------------------------------

    entities = extract_entities(text)

    # -------------------------------
    # 4. Semantic validation
    # -------------------------------

    validation = validate_document(
        text,
        entities,
        intent
    )

    # -------------------------------
    # 5. Return complete result
    # -------------------------------

    return {
        "message": "Document validated successfully",

        "filename": file.filename,

        "intent": intent,

        "extracted_text": text,

        "entities": entities,

        "validation": validation
    }