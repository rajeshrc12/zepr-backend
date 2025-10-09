from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
import os

# Ensure SQLite folder exists for dev
if settings.ENV == "dev":
    db_path = settings.DATABASE_URL_DEV.replace("sqlite:///", "")
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

engine = create_engine(settings.DATABASE_URL, echo=True)


def init_db():
    """Initialize database: create tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def close_db():
    """Close database connections / dispose engine."""
    engine.dispose()


def get_session():
    """Provide a SQLModel session for dependency injection."""
    with Session(engine) as session:
        yield session
