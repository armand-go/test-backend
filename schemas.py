from typing import Optional, Dict
from uuid import UUID
from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class MatchResult(str, Enum):
    player1 = "PLAYER1"
    draw = "DRAW"
    player2 = "PLAYER2"


class MatchCreate(BaseModel):
    player_one_id: Optional[UUID] = None
    player_two_id: Optional[UUID] = None


class Match(MatchCreate):
    id: UUID
    result: MatchResult
    score_one: int = 0
    score_two: int = 0

    class Config:
        orm_mode = True


class MatchUpdate(MatchCreate):
    result: Optional[MatchResult] = None
    score_one: Optional[int] = None
    score_two: Optional[int] = None


class UserCreate(BaseModel):
    username: str = None
    phone_number: str = None


class UserUpdate(UserCreate):
    points: Optional[int] = None


class User(UserCreate):
    id: UUID
    points: int = 0
    matches_as_player_one: list[Match]
    matches_as_player_two: list[Match]

    class Config:
        orm_mode = True


class TournamentCreateUpdate(BaseModel):
    max_player: Optional[int] = None
    begin: datetime
    end: datetime
    rewards_range: Optional[Dict[str, int]] = None


class Tournament(TournamentCreateUpdate):
    id: UUID
    rewards_sum: int

    class Config:
        orm_mode = True
