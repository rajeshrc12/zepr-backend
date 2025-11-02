from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.csv import Csv
from typing import Optional


class MessageBase(BaseModel):
    content: str
    sql: Optional[str] = None
    table: Optional[list] = None
    chart: Optional[dict] = None
    summary: Optional[str] = None
    chat_id: int


class MessageCreate(MessageBase):
    type: str
    pass


class MessageRequest(MessageBase):
    csv: Csv
    pass


class MessageUpdate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    type: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
