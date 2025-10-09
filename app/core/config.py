import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENV: str = os.getenv("ENV", "dev")
    DATABASE_URL_DEV: str = os.getenv("DATABASE_URL_DEV", "sqlite:///./app.db")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    SESSION_SECRET_KEY: str = os.getenv("SESSION_SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 3600))
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    @property
    def DATABASE_URL(self) -> str:
        """Use SQLite for dev, or prod DB for production."""
        if self.ENV == "prod" and self.DATABASE_URL:
            return self.DATABASE_URL
        return self.DATABASE_URL_DEV


settings = Settings()
