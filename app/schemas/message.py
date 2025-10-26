from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MessageBase(BaseModel):
    text: str
    chat_id: int


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
