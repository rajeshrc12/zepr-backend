from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.message import Message, MessageCreate, MessageUpdate
from app.crud.message import create_message, get_messages, get_message, update_message, delete_message

router = APIRouter(prefix="/message", tags=["Message"])


@router.post("/", response_model=Message)
def add_message(message: MessageCreate, db: Session = Depends(get_db)):
    """Create a new message"""
    return create_message(db, message)


@router.get("/", response_model=list[Message])
def read_messages(db: Session = Depends(get_db)):
    """Retrieve all messages"""
    return get_messages(db)


@router.get("/{message_id}", response_model=Message)
def read_message(message_id: int, db: Session = Depends(get_db)):
    """Retrieve a single message by ID"""
    db_message = get_message(db, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message


@router.put("/{message_id}", response_model=Message)
def modify_message(message_id: int, message: MessageUpdate, db: Session = Depends(get_db)):
    """Update an existing message"""
    db_message = update_message(db, message_id, message)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message


@router.delete("/{message_id}", response_model=Message)
def remove_message(message_id: int, db: Session = Depends(get_db)):
    """Delete a message by ID"""
    db_message = delete_message(db, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message
