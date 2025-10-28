from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.message import Message


class ChatBase(BaseModel):
    name: str
    csv_id: int
    user_id: int


class ChatRequest(BaseModel):
    csv_id: int
    message: str


class ChatCreate(ChatBase):
    pass


class ChatUpdate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    created_at: datetime
    messages: list[Message]
    model_config = ConfigDict(from_attributes=True)
