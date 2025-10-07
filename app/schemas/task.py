from typing import Optional
from sqlmodel import SQLModel


class TaskCreate(SQLModel):
    name: str


class TaskUpdate(SQLModel):
    name: Optional[str] = None
    is_completed: Optional[bool] = None
