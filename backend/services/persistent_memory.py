# backend/services/persistent_memory.py

from backend.db.database import SessionLocal

from backend.models.conversation import (
    Conversation
)


def save_message(
        session_id: str,
        role: str,
        content: str
):
    """
    Save conversation message.
    """

    db = SessionLocal()

    message = Conversation(

        session_id=session_id,

        role=role,

        content=content
    )

    db.add(
        message
    )

    db.commit()

    db.close()


def get_messages(
        session_id: str
):
    """
    Retrieve conversation history.
    """

    db = SessionLocal()

    rows = db.query(
        Conversation
    ).filter(

        Conversation.session_id == session_id

    ).all()

    db.close()

    history = []

    for row in rows:

        history.append(

            {

                "role": row.role,

                "content": row.content

            }

        )

    return history


def clear_messages(
        session_id: str
):
    """
    Delete conversation history.
    """

    db = SessionLocal()

    db.query(
        Conversation
    ).filter(

        Conversation.session_id == session_id

    ).delete()

    db.commit()

    db.close()