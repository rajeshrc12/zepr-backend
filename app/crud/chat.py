from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.schemas.chat import ChatUpdate, ChatCreate
from sqlalchemy import desc


def get_chats(db: Session, user_id: int):
    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id)
        .order_by(desc(Chat.created_at))
        .limit(10)
        .all()
    )


def get_chat(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()


def create_chat(db: Session, chat: ChatCreate):
    db_chat = Chat(**chat.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def update_chat(db: Session, chat_id: int, chat: ChatUpdate):
    db_chat = get_chat(db, chat_id)
    if not db_chat:
        return None
    db_chat.name = chat.name
    db_chat.type = chat.type
    db_chat.user_id = chat.user_id
    db.commit()
    db.refresh(db_chat)
    return db_chat


def delete_chat(db: Session, chat_id: int):
    db_chat = get_chat(db, chat_id)
    if not db_chat:
        return None
    db.delete(db_chat)
    db.commit()
    return db_chat
