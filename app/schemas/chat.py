from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.message import Message
from app.schemas.csv import Csv


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
    csv: Csv
    model_config = ConfigDict(from_attributes=True)
