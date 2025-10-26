from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    type = Column(String, nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    owner = relationship("Chat", back_populates="messages")
