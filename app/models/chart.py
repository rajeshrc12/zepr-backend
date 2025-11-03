from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.dialects.postgresql import JSONB


class Chart(Base):
    __tablename__ = "charts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sql = Column(String, nullable=True)
    table = Column(JSONB, nullable=True)
    config = Column(JSONB, nullable=True)
    summary = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
