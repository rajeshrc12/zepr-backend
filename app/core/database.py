from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

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
