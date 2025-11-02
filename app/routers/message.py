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

router = APIRouter(prefix="/message", tags=["Message"])


@router.post("/")
def add_message(message_request: MessageRequest, db: Session = Depends(get_db)):
    """Create a new message_request"""
    content = message_request.content
    chat_id = message_request.chat_id
    csv = message_request.csv
    system_prompt = get_data_analyst_prompt(csv)
    print(system_prompt)
    response = llm.invoke(
        [SystemMessage(system_prompt),
         HumanMessage(content)]
    )
    db_messages = create_messages(
        db, [
            {"type": "human", "content": content,
                "chat_id": chat_id},
            {"type": "ai", "content": response.content,
                "chat_id": chat_id}
        ])
    return db_messages


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
