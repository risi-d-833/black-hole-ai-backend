from fastapi import FastAPI

app = FastAPI(
    title="BLACK HOLE AI",
    description="BLACK HOLE AI Backend API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "BLACK HOLE AI Backend is Online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "BLACK HOLE AI"
    }