# backend/services/persistent_summary.py

from backend.db.database import SessionLocal

from backend.models.conversation_summary import (
    ConversationSummary
)


def save_summary(
        session_id: str,
        summary: str
):
    """
    Save conversation summary.
    """

    db = SessionLocal()

    row = db.query(
        ConversationSummary
    ).filter(

        ConversationSummary.session_id == session_id

    ).first()

    if row:

        row.summary = summary

    else:

        row = ConversationSummary(

            session_id=session_id,

            summary=summary
        )

        db.add(
            row
        )

    db.commit()

    db.close()


def get_summary(
        session_id: str
):
    """
    Retrieve conversation summary.
    """

    db = SessionLocal()

    row = db.query(
        ConversationSummary
    ).filter(

        ConversationSummary.session_id == session_id

    ).first()

    db.close()

    if row:

        return row.summary

    return ""


def clear_summary(
        session_id: str
):
    """
    Remove summary.
    """

    db = SessionLocal()

    db.query(
        ConversationSummary
    ).filter(

        ConversationSummary.session_id == session_id

    ).delete()

    db.commit()

    db.close()