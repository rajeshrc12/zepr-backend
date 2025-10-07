import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    SESSION_SECRET_KEY: str = os.getenv("SESSION_SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    FRONTEND_URL: int = os.getenv("FRONTEND_URL")


settings = Settings()
