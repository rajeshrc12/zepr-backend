from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_or_create_user(db: Session, user_data: UserCreate) -> User:
    """
    Get an existing user by email or create a new one.
    """
    db_user = db.query(User).filter(User.email == user_data.email).first()

    if not db_user:
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            image=user_data.image
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    return db_user


def get_user(db: Session, user_id: str) -> User:
    """
    Get a user by ID. Raises 404 if not found.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
