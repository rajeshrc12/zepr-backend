from sqlalchemy.orm import Session
from app.models.message import Message
from app.schemas.message import MessageUpdate, MessageCreate


def get_messages(db: Session):
    return db.query(Message).all()


def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()


def create_message(db: Session, message: MessageCreate):
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_message(db: Session, message_id: int, message: MessageUpdate):
    db_message = get_message(db, message_id)
    if not db_message:
        return None
    db_message.text = message.text
    db_message.chat_id = message.chat_id
    db.commit()
    db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: int):
    db_message = get_message(db, message_id)
    if not db_message:
        return None
    db.delete(db_message)
    db.commit()
    return db_message
