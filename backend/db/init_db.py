from backend.db.database import engine
from backend.models.base import Base

# Import models
from backend.models.appointment import Appointment
from backend.models.user import User

from backend.models.conversation import Conversation
from backend.models.conversation_summary import ConversationSummary


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")