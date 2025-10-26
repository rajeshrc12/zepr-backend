from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    csv_id = Column(Integer, ForeignKey("csvs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)

    owner = relationship("User", back_populates="chats")
    csv = relationship("Csv", back_populates="chats")

    messages = relationship("Message", back_populates="owner")
