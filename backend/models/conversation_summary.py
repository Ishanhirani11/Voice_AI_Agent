# backend/models/conversation_summary.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from backend.models.base import Base


class ConversationSummary(Base):

    __tablename__ = "conversation_summaries"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    summary = Column(
        Text,
        nullable=False
    )