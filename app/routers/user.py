from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.user import create_user, get_user
from app.schemas.user import User, UserCreate
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=User)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return create_user(db, user)


@router.get("/", response_model=User)
def read_user(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve a single user by ID"""
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user
