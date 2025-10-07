from typing import Optional
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    name: str
    email: str
    image: Optional[str] = None


class UserRead(SQLModel):
    id: int
    name: str
    email: str
    image: Optional[str] = None
