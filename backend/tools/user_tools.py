# backend/tools/user_tools.py

from backend.db.database import SessionLocal
from backend.models.user import User


def identify_user(
        name: str,
        phone: str
) -> dict:
    """
    Identify or register a user by phone number.
    """

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.phone == phone
        ).first()

        if user:
            return {
                "success": True,
                "message": f"Welcome back, {user.name}!",
                "name": user.name
            }

        new_user = User(
            name=name,
            phone=phone
        )

        db.add(new_user)
        db.commit()

        return {
            "success": True,
            "message": f"Welcome, {name}! You have been registered."
        }

    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": f"Failed to identify user: {str(e)}"
        }

    finally:
        db.close()


def end_conversation() -> dict:
    """
    Signal end of conversation.
    """

    return {
        "success": True,
        "message": "Conversation ended. Generating summary."
    }