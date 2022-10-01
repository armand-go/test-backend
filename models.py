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

    matches = relationship("Match")

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
    player_one_id = Column(UUID, ForeignKey("users.id"))
    player_one = relationship("User", back_populates="matches")
    player_two_id = Column(UUID, ForeignKey("users.id"))
    player_two = relationship("User", back_populates="matches")
    result = Column(Enum(MatchResultEnum), default=MatchResultEnum.draw, nullable=False)
    score_one = Column(Integer, default=0)
    score_two = Column(Integer, default=0)
