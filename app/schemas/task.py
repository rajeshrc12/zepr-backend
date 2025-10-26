from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
