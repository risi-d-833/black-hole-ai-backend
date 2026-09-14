from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai import generate_ai_response


# =========================================================
# BLACK HOLE AI - FastAPI Application
# =========================================================

app = FastAPI(
    title="BLACK HOLE AI",
    description="BLACK HOLE AI Personal Agent Backend",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://black-hole-ai.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# REQUEST MODEL
# =========================================================

class ChatRequest(BaseModel):
    message: str


# =========================================================
# ROOT
# =========================================================

@app.get("/")
async def root():
    return {
        "success": True,
        "message": "BLACK HOLE AI Backend is Online",
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():
    return {
        "success": True,
        "status": "healthy",
        "service": "BLACK HOLE AI",
    }


# =========================================================
# SERVER STATUS
# =========================================================

@app.get("/api/status")
async def status():
    return {
        "success": True,
        "name": "BLACK HOLE AI",
        "backend": "FastAPI",
        "ai": "Gemini",
        "status": "online",
    }


# =========================================================
# CHAT API
# =========================================================

@app.post("/api/chat")
async def chat(request: ChatRequest):

    # Check empty message
    if not request.message.strip():
        return {
            "success": False,
            "error": "Message cannot be empty",
        }

    try:

        # Send message to AI
        response = await generate_ai_response(
            request.message
        )

        return {
            "success": True,
            "message": request.message,
            "response": response,
        }

    except Exception as error:

        # Print complete error in terminal
        print("=" * 60)
        print("BLACK HOLE AI ERROR")
        print(repr(error))
        print("=" * 60)

        # Return error for testing
        return {
            "success": False,
            "error": str(error),
        }