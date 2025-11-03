from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import Chat, ChatUpdate, ChatRequest, ChatBase
from app.schemas.message import MessageCreate
from app.crud.chat import create_chat, get_chats, get_chat, update_chat, delete_chat
from app.crud.message import create_message
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=Chat)
def add_chat(chat_request: ChatRequest, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new chat"""
    name = "Test chat"
    csv_id = chat_request.csv_id
    message = chat_request.message
    chat_base = ChatBase(
        name=name,
        csv_id=csv_id,
        user_id=user_id
    )
    chat = create_chat(db, chat_base)
    chat_id = chat.id

    message_create = MessageCreate(
        type="human",
        content=message,
        chat_id=chat_id
    )
    create_message(db, message_create)
    return chat


@router.get("/", response_model=list[Chat])
def read_chats(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all chats"""
    return get_chats(db, user_id)


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
