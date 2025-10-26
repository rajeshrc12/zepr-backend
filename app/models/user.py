from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    image = Column(String, nullable=False)
    credits = Column(Integer, default=10, nullable=False)
    created_at = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)
    connections = relationship("Connection", back_populates="owner")
    csvs = relationship("Csv", back_populates="owner")
