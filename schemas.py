from typing import Optional
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, Field


class MatchResult(str, Enum):
    palyer1 = "PLAYER1"
    draw = "DRAW"
    player2 = "PLAYER2"


class MatchCreate(BaseModel):
    player_one_id: Optional[UUID] = None
    player_two_id: Optional[UUID] = None

class MatchBase(MatchCreate):
    id: UUID
    result: MatchResult = Field(MatchResult.draw, alias='Result')
    score_one: int = 0
    score_two: int = 0

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str = None
    phone_number: str = None


class UserUpdate(UserBase):
    points: Optional[int] = 0


class User(UserBase):
    id: UUID
    points: int = 0
    matches_as_player_one: list[MatchBase]
    matches_as_player_two: list[MatchBase]

    class Config:
        orm_mode = True
