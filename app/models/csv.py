from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone
from app.core.database import Base


class Csv(Base):
    __tablename__ = "csvs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    columns = Column(JSONB, nullable=True)
    owner = relationship("User", back_populates="csvs")
    chats = relationship("Chat", back_populates="csv")
