from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import models
import schemas


def create_user(db: Session, user: schemas.User):
    try:
        db_user = models.User(username=user.username, phone_number=user.phone_number)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except AssertionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user(db: Session, user_id: UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, db_user: schemas.User, user_data: schemas.UserUpdate):
    user_data_dict = user_data.dict(exclude_unset=True)
    for key, value in user_data_dict.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: schemas.User):
    db.delete(db_user)
    db.commit()


def create_match(db: Session, match: schemas.Match):
    db_match = models.Match(
        player_one_id=match.player_one_id,
        player_two_id=match.player_two_id,
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def get_match(db: Session, match_id: UUID):
    return db.query(models.Match).filter(models.Match.id == match_id).first()


def update_match(db: Session, db_match: schemas.Match, match_data: schemas.MatchUpdate):
    match_data_dict = match_data.dict(exclude_unset=True)
    for key, value in match_data_dict.items():
        setattr(db_match, key, value)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def delete_match(db: Session, db_match: schemas.Match):
    db.delete(db_match)
    db.commit()
