from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.message import Message, MessageBase, MessageUpdate
from app.crud.message import get_messages, get_message, update_message, delete_message, create_messages
from app.services.openai import llm
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
router = APIRouter(prefix="/message", tags=["Message"])

messages = []


@router.post("/")
def add_message(message: MessageBase, db: Session = Depends(get_db)):
    """Create a new message"""
    messages.append(HumanMessage(message.content))
    response = llm.invoke(
        [SystemMessage("You are AI Data Analyst")]+messages
    )
    messages.append(AIMessage(response.content))
    db_messages = create_messages(
        db, [
            {"type": "human", "content": message.content, "chat_id": message.chat_id},
            {"type": "ai", "content": response.content, "chat_id": message.chat_id}
        ])
    return db_messages


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
