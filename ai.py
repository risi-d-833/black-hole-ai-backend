import os

from dotenv import load_dotenv
from google import genai


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured in .env"
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# BLACK HOLE AI
# =========================================================

async def generate_ai_response(message: str) -> str:

    if not message or not message.strip():
        return "Please enter a message."

    try:

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=message,
        )

        # Current Interactions API convenience property
        response_text = interaction.output_text

        if not response_text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response_text

    except Exception as error:

        print("=" * 60)
        print("GEMINI AI ERROR")
        print(repr(error))
        print("=" * 60)

        raise