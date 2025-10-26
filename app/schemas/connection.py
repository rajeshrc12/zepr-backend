from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ConnectionBase(BaseModel):
    name: str
    type: str
    user_id: int


class ConnectionCreate(ConnectionBase):
    pass


class ConnectionUpdate(ConnectionBase):
    pass


class Connection(ConnectionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
