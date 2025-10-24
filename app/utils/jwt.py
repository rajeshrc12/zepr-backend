# app/utils/jwt.py
import jwt
from typing import Optional
from app.core.config import settings
from datetime import datetime, timezone, timedelta


def create_jwt(user_id: int):
    expire = datetime.now(
        timezone.utc) + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": str(user_id), "exp": expire}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY,
                       algorithm=settings.ALGORITHM)
    return token


def decode_jwt(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
