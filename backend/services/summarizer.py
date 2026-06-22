# backend/services/summarizer.py

import time

from backend.services.llm import chat_with_llm


def generate_summary(
        history: list[dict]
) -> str:
    """
    Generate a conversation summary using LLM.

    Returns a structured summary including:
    - Patient name and phone number
    - Appointments booked, cancelled, or modified
    - User preferences
    - Timestamp
    """

    timestamp = time.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    messages = [
        {
            "role": "system",
            "content": f"""
Summarize this healthcare receptionist conversation.

Return a JSON object with:
{{
    "summary": "Brief overview of the conversation",
    "patient_name": "Name if provided, else null",
    "phone_number": "Phone if provided, else null",
    "appointments_booked": ["list of booked appointments with date and time"],
    "appointments_cancelled": ["list of cancelled appointments"],
    "appointments_modified": ["list of modified appointments"],
    "user_preferences": ["any stated preferences"],
    "timestamp": "{timestamp}"
}}

Include only information explicitly discussed.
Output raw JSON only.
"""
        }
    ]

    messages.extend(history)

    try:
        return chat_with_llm(messages)
    except Exception:
        return '{{"summary": "Unable to generate summary.", "timestamp": "' + timestamp + '"}}'