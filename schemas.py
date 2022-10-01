from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str = None
    phone_number: str = None


class UserUpdate(UserBase):
    points: Optional[int] = None


class User(UserBase):
    id: UUID
    points: int

    class Config:
        orm_mode = True
