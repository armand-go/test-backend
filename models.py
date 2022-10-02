from sqlalchemy.orm import validates, relationship
from sqlalchemy import (
    Column, String, Integer, ForeignKey, Enum, DateTime, Table
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
import datetime as D
import uuid
import re

Base = declarative_base()

tournament_user = Table(
    "tournament_user",
    Base.metadata,
    Column("tournament_id", ForeignKey("tournaments.id")),
    Column("user_id", ForeignKey("users.id"))
)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    phone_number = Column(String)
    points = Column(Integer, default=0)

    matches_as_player_one = relationship(
        "Match", foreign_keys='Match.player_one_id', back_populates="player_one"
    )
    matches_as_player_two = relationship(
        "Match", foreign_keys='Match.player_two_id', back_populates="player_two"
    )

    tournaments_registered = relationship(
        "Tournament", secondary=tournament_user, back_populates="player_list"
    )

    @validates('username')
    def validate_username(self, _key, value):
        value_stripped = value.strip()
        assert len(value_stripped) >= 3 and len(value_stripped) <= 38, \
            "Username must be between 3 and 38 characters"

        return value_stripped

    @validates('phone_number')
    def validate_phone(self, _key, value):
        value_stripped = value.strip()
        assert re.match("(^[0-9]{10}$)", value_stripped), "Incorrect phone number."
        return value_stripped


class Match(Base):
    __tablename__ = "matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    player_one_id = Column(UUID(as_uuid=True), ForeignKey(User.id), default=None)
    player_one = relationship(
        "User", foreign_keys=[player_one_id], back_populates="matches_as_player_one"
    )
    player_two_id = Column(UUID(as_uuid=True), ForeignKey(User.id), default=None)
    player_two = relationship(
        "User", foreign_keys=[player_two_id], back_populates="matches_as_player_two"
    )

    result = Column(
        Enum("PLAYER1", "DRAW", "PLAYER2", name="result", create_type=False),
        default="DRAW", nullable=False
    )
    score_one = Column(Integer, default=0)
    score_two = Column(Integer, default=0)


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    max_player = Column(Integer, default=20)
    player_list = relationship(
        "User", secondary=tournament_user, back_populates="tournaments_registered"
    )
    players_score = Column(JSONB, default={})

    begin = Column(
        DateTime(timezone=True),
        nullable=False,
        default=D.datetime.now() + D.timedelta(minutes=30)
    )
    end = Column(
        DateTime(timezone=True),
        nullable=False,
        default=D.datetime.now() + D.timedelta(hours=1)
    )

    rewards_sum = Column(Integer, default=0)
    rewards_range = Column(JSONB, default={})

    def leaderboard(self):
        leaderboard = []
        for key, value in self.players_score.items():
            leaderboard.append([key, value])

        # Bubble Sort
        length = len(leaderboard)
        for i in range(0, length):
            for j in range(0, length - i - 1):
                if (leaderboard[j][1] > leaderboard[j + 1][1]):
                    temp = leaderboard[j]
                    leaderboard[j] = leaderboard[j + 1]
                    leaderboard[j + 1] = temp
        leaderboard.reverse()  # Descending order
        return leaderboard

    @validates('rewards_range')
    def validate_rewards_range(self, _key, value):
        for key in value.keys():
            assert re.match("(^[0-9]{1,2}-[0-9]{1,2}$)", key), \
                f"The key {key} doesn't have the correct format (should be X-Y)"
        return value
