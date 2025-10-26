from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone
from app.core.database import Base


class Csv(Base):
    __tablename__ = "csvs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    file_name = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    columns = Column(JSONB, nullable=True)
    owner = relationship("User", back_populates="csvs")
