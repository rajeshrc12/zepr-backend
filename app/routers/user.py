from fastapi import APIRouter, Depends
from app.core.database import get_session
from app.crud.user import (
    get_user
)
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/user", tags=["user"])


@router.get("/")
def get_me(user_id: str = Depends(get_current_user), session=Depends(get_session)):
    print("get_me", user_id)
    return get_user(user_id, session)
