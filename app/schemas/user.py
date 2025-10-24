from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: str
    image: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    credits: int

    class Config:
        orm_mode = True
