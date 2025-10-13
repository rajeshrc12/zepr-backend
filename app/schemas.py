from pydantic import BaseModel, Field
from datetime import datetime


class TaskBase(BaseModel):
    name: str
    is_completed: bool = False
    due_date: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
