# app/utils/jwt.py
from datetime import datetime, timedelta
import jwt
from app.core.config import settings


def create_jwt(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": str(user_id), "exp": expire}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY,
                       algorithm=settings.ALGORITHM)
    return token
