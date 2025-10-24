from pydantic import BaseModel
from datetime import datetime


class TaskBase(BaseModel):
    name: str
    is_completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    due_date: datetime

    class Config:
        orm_mode = True
