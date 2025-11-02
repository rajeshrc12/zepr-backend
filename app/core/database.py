from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from dotenv import load_dotenv
from app.core.config import settings

load_dotenv()

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create engine with safe connection handling
engine_csv = create_engine(
    settings.DATABASE_CSV_URL,
    pool_pre_ping=True,    # ✅ Ensures stale connections are checked
    pool_recycle=1800,     # ✅ Recycles connections every 30 mins
    pool_size=5,           # Optional: adjust for load
    max_overflow=10,       # Optional: allows bursts
    echo=False,            # Set True only for debugging
)

# Use scoped_session to handle threading safely
SessionCSV = scoped_session(sessionmaker(bind=engine_csv))
