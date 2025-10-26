from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChatBase(BaseModel):
    name: str
    csv_id: int
    user_id: int


class ChatCreate(ChatBase):
    pass


class ChatUpdate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
