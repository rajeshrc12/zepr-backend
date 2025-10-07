from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate


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
