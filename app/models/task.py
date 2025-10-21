from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    due_date = Column(DateTime, default=datetime.utcnow, nullable=False)
