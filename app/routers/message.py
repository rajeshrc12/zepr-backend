from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.message import Message, MessageRequest, MessageUpdate, MessageCreate
from app.crud.message import get_messages, get_message, update_message, delete_message, create_messages, create_message
from app.services.langgraph import chatbot
from fastapi.responses import StreamingResponse
from app.utils.prompt import get_data_analyst_prompt
from langchain_core.messages import HumanMessage, SystemMessage
from app.services.openai import llm
import json
from app.core.dependencies import get_current_user
from app.services.agent import chatbot
from app.services.python_sandbox import execute_code

router = APIRouter(prefix="/message", tags=["Message"])


@router.post("/")
def add_message(message_request: MessageRequest, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new message_request"""
    user_query = message_request.content
    chat_id = message_request.chat_id
    csv_id = message_request.csv_id
    csv_columns = message_request.csv_columns
    csv_name = message_request.csv_name
    result = chatbot.invoke({
        "chat_id": chat_id,
        "user_query": user_query,
        "user_id": user_id,
        "csv_id": csv_id,
        "csv_columns": csv_columns,
        "csv_name": csv_name,
        "response": {},
        "output": []
    })
    return result


@router.get("/stream")
async def stream_message(
    chat_id: str = Query(...),
    content: str = Query(...),
    csv: str = Query(...),
):
    print(csv)

    async def event_generator():
        async for event in chatbot.astream({
            "chat_id": chat_id,
            "message": content,
            "csv": json.loads(csv),
            "query": "",
            "content": "",
            "sql": "",
            "table": [],
            "chart": {},
            "summary": "",
        }):
            yield f"data: {json.dumps(event)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


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
