# backend/services/memory.py

from backend.config import MAX_HISTORY


conversation_history: dict[str, list[dict]] = {}


def add_message(
        session_id: str,
        role: str,
        content: str
) -> None:
    """
    Add a message to conversation history.
    Enforces MAX_HISTORY limit.
    """

    if session_id not in conversation_history:
        conversation_history[session_id] = []

    conversation_history[session_id].append(
        {
            "role": role,
            "content": content
        }
    )

    # Enforce history limit
    if len(conversation_history[session_id]) > MAX_HISTORY:
        conversation_history[session_id] = \
            conversation_history[session_id][-MAX_HISTORY:]


def get_history(
        session_id: str
) -> list[dict]:
    """
    Retrieve conversation history for a session.
    """

    if session_id not in conversation_history:
        return []

    return conversation_history[session_id]


def clear_history(
        session_id: str
) -> None:
    """
    Clear conversation history for a session.
    """

    conversation_history[session_id] = []