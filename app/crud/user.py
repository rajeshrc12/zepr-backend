from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.user import User


def get_or_create_user(user_data: UserCreate, session: Session) -> User:
    """
    Get an existing user by email or create a new one.
    """
    statement = select(User).where(User.email == user_data.email)
    db_user = session.exec(statement).first()

    if not db_user:
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            image=user_data.image
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

    return db_user


def get_user(user_id: str, session: Session) -> User:
    print("get_user")
    statement = select(User).where(User.id == user_id)
    db_user = session.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
