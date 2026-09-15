from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai import generate_ai_response
from database import (
    create_conversation,
    save_message,
    get_conversation_messages,
)


# =========================================================
# BLACK HOLE AI - FastAPI Application
# =========================================================

app = FastAPI(
    title="BLACK HOLE AI",
    description="BLACK HOLE AI Personal Agent Backend",
    version="1.0.0",
)


# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# REQUEST MODELS
# =========================================================

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []
    conversation_id: int | None = None


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
        "model": "gemini-3.6-flash",
        "database": "PostgreSQL",
        "status": "online",
    }


# =========================================================
# GET SAVED CONVERSATION
# =========================================================

@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: int):

    try:

        messages = get_conversation_messages(
            conversation_id
        )

        return {
            "success": True,
            "conversation_id": conversation_id,
            "messages": messages,
        }

    except Exception as error:

        print("=" * 60)
        print("GET CONVERSATION ERROR")
        print(repr(error))
        print("=" * 60)

        return {
            "success": False,
            "error": str(error),
        }


# =========================================================
# CHAT API
# =========================================================

@app.post("/api/chat")
async def chat(request: ChatRequest):

    # -----------------------------------------------------
    # Validate message
    # -----------------------------------------------------

    if not request.message.strip():
        return {
            "success": False,
            "error": "Message cannot be empty",
        }

    try:

        # -------------------------------------------------
        # Use existing conversation OR create new one
        # -------------------------------------------------

        conversation_id = request.conversation_id

        if conversation_id is None:

            conversation_id = create_conversation(
                user_id=1,
                title=request.message[:50],
            )

        # -------------------------------------------------
        # Convert frontend history
        # -------------------------------------------------

        history = [
            {
                "role": item.role,
                "content": item.content,
            }
            for item in request.history
            if item.role in ["user", "assistant"]
            and item.content
        ]

        # -------------------------------------------------
        # Save user message
        # -------------------------------------------------

        save_message(
            conversation_id=conversation_id,
            role="user",
            content=request.message.strip(),
        )

        # -------------------------------------------------
        # Generate AI response
        # -------------------------------------------------

        response = await generate_ai_response(
            message=request.message,
            history=history,
        )

        # -------------------------------------------------
        # Save AI response
        # -------------------------------------------------

        save_message(
            conversation_id=conversation_id,
            role="assistant",
            content=response,
        )

        # -------------------------------------------------
        # Return response
        # -------------------------------------------------

        return {
            "success": True,
            "conversation_id": conversation_id,
            "message": request.message,
            "response": response,
        }

    except Exception as error:

        print("=" * 60)
        print("BLACK HOLE AI ERROR")
        print(repr(error))
        print("=" * 60)

        return {
            "success": False,
            "error": str(error),
        }