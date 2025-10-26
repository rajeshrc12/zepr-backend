from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import Chat, ChatCreate, ChatUpdate
from app.crud.chat import create_chat, get_chats, get_chat, update_chat, delete_chat

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=Chat)
def add_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    """Create a new chat"""
    return create_chat(db, chat)


@router.get("/", response_model=list[Chat])
def read_chats(db: Session = Depends(get_db)):
    """Retrieve all chats"""
    return get_chats(db)


@router.get("/{chat_id}", response_model=Chat)
def read_chat(chat_id: int, db: Session = Depends(get_db)):
    """Retrieve a single chat by ID"""
    db_chat = get_chat(db, chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat


@router.put("/{chat_id}", response_model=Chat)
def modify_chat(chat_id: int, chat: ChatUpdate, db: Session = Depends(get_db)):
    """Update an existing chat"""
    db_chat = update_chat(db, chat_id, chat)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat


@router.delete("/{chat_id}", response_model=Chat)
def remove_chat(chat_id: int, db: Session = Depends(get_db)):
    """Delete a chat by ID"""
    db_chat = delete_chat(db, chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat
