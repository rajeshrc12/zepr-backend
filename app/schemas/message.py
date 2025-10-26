from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MessageBase(BaseModel):
    content: str
    chat_id: int


class MessageCreate(MessageBase):
    type: str
    pass


class MessageUpdate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    type: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
