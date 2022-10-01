from sqlalchemy.orm import validates
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True)
    points = Column(Integer, default=0)

    @validates('username')
    def validate_username(self, _key, value):
        value_stripped = value.strip()
        assert len(value_stripped) >= 3 and len(value_stripped) <= 38, \
            "Username must be between 3 and 38 characters"

        return value_stripped.strip()


class Match(Base):
    __tablename__ = "matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # player_one
    # player_2
    # result
    # score
