from fastapi import FastAPI

app = FastAPI(
    title="Semantic Validation Framework",
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