from email.policy import default
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import enum

import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True)
    points = Column(Integer, default=0)

    matches_as_player_one = relationship(
        "Match", foreign_keys='Match.player_one_id', back_populates="player_one"
    )
    matches_as_player_two = relationship(
        "Match", foreign_keys='Match.player_two_id', back_populates="player_two"
    )

    @validates('username')
    def validate_username(self, _key, value):
        value_stripped = value.strip()
        assert len(value_stripped) >= 3 and len(value_stripped) <= 38, \
            "Username must be between 3 and 38 characters"

        return value_stripped.strip()


class MatchResultEnum(enum.Enum):
    palyer1 = "PLAYER1"
    draw = "DRAW"
    player2 = "PLAYER2"


class Match(Base):
    __tablename__ = "matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    player_one_id = Column(UUID, ForeignKey(User.id), default=None)
    player_one = relationship(
        "User", foreign_keys=[player_one_id], back_populates="matches_as_player_one"
    )
    player_two_id = Column(UUID, ForeignKey(User.id), default=None)
    player_two = relationship(
        "User", foreign_keys=[player_two_id], back_populates="matches_as_player_two"
    )

    result = Column(Enum(MatchResultEnum), default=MatchResultEnum.draw, nullable=False)
    score_one = Column(Integer, default=0)
    score_two = Column(Integer, default=0)
