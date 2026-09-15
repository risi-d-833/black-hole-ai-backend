import os

import psycopg
from dotenv import load_dotenv


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured in .env"
    )


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return psycopg.connect(DATABASE_URL)


# =========================================================
# CREATE CONVERSATION
# =========================================================

def create_conversation(
    user_id: int,
    title: str,
):
    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO conversations
                (user_id, title)
                VALUES (%s, %s)
                RETURNING id
                """,
                (
                    user_id,
                    title,
                ),
            )

            conversation_id = cursor.fetchone()[0]

        conn.commit()

    return conversation_id


# =========================================================
# SAVE MESSAGE
# =========================================================

def save_message(
    conversation_id: int,
    role: str,
    content: str,
):
    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO messages
                (conversation_id, role, content)
                VALUES (%s, %s, %s)
                """,
                (
                    conversation_id,
                    role,
                    content,
                ),
            )

        conn.commit()


# =========================================================
# GET CONVERSATION MESSAGES
# =========================================================

def get_conversation_messages(
    conversation_id: int,
):
    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    role,
                    content,
                    created_at
                FROM messages
                WHERE conversation_id = %s
                ORDER BY id ASC
                """,
                (
                    conversation_id,
                ),
            )

            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "role": row[1],
            "content": row[2],
            "created_at": row[3].isoformat()
            if row[3]
            else None,
        }
        for row in rows
    ]