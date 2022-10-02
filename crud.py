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


def get_user_by_phone_number(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()


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


def create_tournament(db: Session, tournament: schemas.TournamentCreateUpdate):
    try:
        rewards_sum = 0
        for key, value in tournament.rewards_range.items():
            (inf, sup) = key.split('-')
            multiplier = int(sup) - int(inf) + 1
            rewards_sum += value * multiplier

        db_tournament = models.Tournament(
            max_player=tournament.max_player,
            begin=tournament.begin,
            end=tournament.end,
            rewards_sum=rewards_sum,
            rewards_range=tournament.rewards_range
        )
        db.add(db_tournament)
        db.commit()
        db.refresh(db_tournament)
    except AssertionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e) + ". Check the range has the correct format."
        )
    return db_tournament


def get_tournament(db: Session, tournament_id: UUID):
    return db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()


def get_tournaments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tournament).offset(skip).limit(limit).all()


def update_tournament(
    db: Session,
    db_tournament: schemas.Tournament,
    tournament_data: schemas.TournamentCreateUpdate
):
    tournament_data_dict = tournament_data.dict(exclude_unset=True)
    for key, value in tournament_data_dict.items():
        setattr(db_tournament, key, value)
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


def delete_tournament(db: Session, db_tournament: schemas.Tournament):
    db.delete(db_tournament)
    db.commit()
