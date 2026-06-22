# backend/services/llm.py

from groq import Groq

from backend.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    TEMPERATURE
)


client = Groq(
    api_key=GROQ_API_KEY
)


def chat_with_llm(
        messages: list[dict]
) -> str:
    """
    Send messages to Groq LLM and return response text.

    Uses model and temperature from config.
    Raises exception on failure for caller to handle.
    """

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            response_format={"type": "json_object"}
        )

        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(
            f"LLM call failed: {str(e)}"
        )