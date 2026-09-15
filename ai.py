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

async def generate_ai_response(
    message: str,
    history: list | None = None,
) -> str:

    # -----------------------------------------------------
    # Validate message
    # -----------------------------------------------------

    if not message or not message.strip():

        return "Please enter a message."


    try:

        # =================================================
        # BUILD CONVERSATION
        # =================================================

        conversation = []


        # -------------------------------------------------
        # Add previous conversation
        # -------------------------------------------------

        if history:

            for item in history:

                role = item.get("role")

                content = item.get("content")


                if (
                    role in ["user", "assistant"]
                    and content
                ):

                    conversation.append(
                        f"{role.upper()}: {content}"
                    )


        # -------------------------------------------------
        # Add current user message
        # -------------------------------------------------

        conversation.append(
            f"USER: {message.strip()}"
        )


        # -------------------------------------------------
        # Final prompt
        # -------------------------------------------------

        full_input = "\n\n".join(
            conversation
        )


        # =================================================
        # GEMINI REQUEST
        # =================================================

        interaction = client.interactions.create(

            # ---------------------------------------------
            # Gemini 3.8 Flash
            # ---------------------------------------------

            model="gemini-3.8-flash",

            input=full_input,

        )


        # =================================================
        # GET RESPONSE
        # =================================================

        response_text = (
            interaction.output_text
        )


        # -------------------------------------------------
        # Empty response protection
        # -------------------------------------------------

        if not response_text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )


        return response_text


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as error:

        print("=" * 60)

        print("GEMINI AI ERROR")

        print(repr(error))

        print("=" * 60)


        # -------------------------------------------------
        # Friendly quota error
        # -------------------------------------------------

        error_text = str(error)


        if (
            "429" in error_text
            or "quota" in error_text.lower()
            or "too_many_requests"
            in error_text.lower()
        ):

            raise RuntimeError(
                "BLACK HOLE AI is temporarily busy because "
                "the Gemini API request limit was reached. "
                "Please wait a little and try again."
            )


        # -------------------------------------------------
        # Other errors
        # -------------------------------------------------

        raise RuntimeError(
            f"Gemini AI error: {error_text}"
        )