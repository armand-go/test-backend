from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import engine, SessionLocal
import datetime as D
import models
import schemas
import crud


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already created."
        )
    db_user = crud.get_user_by_phone_number(db=db, phone_number=user.phone_number)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An user with this phone number already exists."
        )
    return crud.create_user(db=db, user=user)


# TODO: Implement pagination and filter
@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> schemas.User:
    users = crud.get_users(db, skip, limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: UUID, db: Session = Depends(get_db)) -> schemas.User:
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


def create_or_get_user(user: schemas.UserCreate, db: Depends(get_db)) -> schemas.User:
    user_db = crud.get_user_by_username(db, username=user.username)
    if user_db:
        return user_db

    user_db = create_user(user, db)
    return user_db


@app.put("/users/update/{user_id}", response_model=schemas.User)
def update_user(
    user_id: UUID,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db)
) -> schemas.User:
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return crud.update_user(db, db_user, user)


# TODO: Delete user shoudln't really delete user, but anonymising it.
@app.delete("/users/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return crud.delete_user(db, db_user)


@app.post("/matches/", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)) -> schemas.Match:
    return crud.create_match(db=db, match=match)


@app.get("/matches/{match_id}", response_model=schemas.Match)
def read_match(match_id: UUID, db: Session = Depends(get_db)) -> schemas.Match:
    match = crud.get_match(db, match_id=match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found.")
    return match


@app.put("/matches/update/{match_id}", response_model=schemas.Match)
def update_match(
    match_id: UUID,
    match: schemas.MatchUpdate,
    db: Session = Depends(get_db)
) -> schemas.Match:
    db_match = crud.get_match(db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found.")
    return crud.update_match(db, db_match, match)


@app.delete("/matches/delete/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: UUID, db: Session = Depends(get_db)):
    db_match = crud.get_match(db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found.")
    return crud.delete_match(db, db_match)


@app.post("/tournaments/", response_model=schemas.Tournament)
def create_tournament(
    tournament: schemas.TournamentCreateUpdate,
    db: Session = Depends(get_db)
) -> schemas.Tournament:
    return crud.create_tournament(db=db, tournament=tournament)


@app.get("/tournaments/", response_model=list[schemas.Tournament])
def read_tournaments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> schemas.Tournament:
    return crud.get_tournaments(db, skip, limit)


@app.get("/tournaments/{tournament_id}", response_model=schemas.Tournament)
def read_tournament(tournament_id: UUID, db: Session = Depends(get_db)) -> schemas.Tournament:
    tournament = crud.get_tournament(db, tournament_id=tournament_id)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found.")
    return tournament


@app.put("/tournaments/update/{tournament_id}", response_model=schemas.Tournament)
def update_tournament(
    tournament_id: UUID,
    tournament: schemas.TournamentCreateUpdate,
    db: Session = Depends(get_db)
) -> schemas.Tournament:
    db_tournament = crud.get_tournament(db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found.")

    if db_tournament.end < D.datetime.now():
        raise HTTPException(status_code=406, detail="Tournament has already ended.")
    elif db_tournament.begin < D.datetime.now():
        raise HTTPException(status_code=406, detail="Tournament has already started.")

    return crud.update_tournament(db, db_tournament, tournament)


@app.delete("/tournaments/delete/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tournament(tournament_id: UUID, db: Session = Depends(get_db)):
    db_tournament = crud.get_tournament(db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found.")
    return crud.delete_tournament(db, db_tournament)


@app.post("/tournaments/{tournament_id}/register", response_model=schemas.Tournament)
def register_to_tournament(
    tournament_id: UUID,
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
) -> schemas.Tournament:
    db_tournament = crud.get_tournament(db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found.")

    if db_tournament.end < D.datetime.now():
        raise HTTPException(status_code=406, detail="Tournament has already ended.")
    elif db_tournament.begin < D.datetime.now():
        raise HTTPException(status_code=406, detail="Tournament has already started.")

    users_registered = (
        db.
        query(models.tournament_user)
        .filter(models.tournament_user.c.tournament_id == tournament_id)
        .count()
    )
    if users_registered < db_tournament.max_player:
        user_to_register = create_or_get_user(user, db)

        is_user_already_registered = (
            db.
            query(models.tournament_user)
            .filter(models.tournament_user.c.user_id == user_to_register.id)
            .filter(models.tournament_user.c.tournament_id == tournament_id)
            .first()
        )
        if is_user_already_registered:
            raise HTTPException(
                status_code=406,
                detail="Already registered in this tournament."
            )

        db_tournament.player_list.append(user_to_register)
        db.add(db_tournament)
        db.commit()
        db.refresh(db_tournament)
    else:
        raise HTTPException(
            status_code=406,
            detail="Too many players registered in this tournament."
        )
    return db_tournament


@app.post("/tournaments/{tournament_id}/match", response_model=schemas.Match)
def initialize_match_between_users(
    tournament_id: UUID,
    player_1_id: UUID,
    player_2_id: UUID,
    db: Session = Depends(get_db)
) -> schemas.Match:
    db_tournament = read_tournament(tournament_id=tournament_id, db=db)
    if db_tournament.end < D.datetime.now():
        raise HTTPException(status_code=406, detail="Tournament has already ended.")
    elif D.datetime.now() < db_tournament.begin:
        raise HTTPException(status_code=406, detail="Tournament has not started yet.")

    read_user(user_id=player_1_id, db=db)
    read_user(user_id=player_1_id, db=db)

    is_player_1_registered = (
        db.
        query(models.tournament_user)
        .filter(models.tournament_user.c.user_id == player_1_id)
        .first()
    )
    if is_player_1_registered is None:
        raise HTTPException(
            status_code=404,
            detail="Player 1 is not registered to this tournament."
        )
    is_player_2_registered = (
        db.
        query(models.tournament_user)
        .filter(models.tournament_user.c.user_id == player_2_id)
        .first()
    )
    if is_player_2_registered is None:
        raise HTTPException(
            status_code=404,
            detail="Player 2 is not registered to this tournament."
        )
    return create_match(
        match=schemas.MatchCreate(
            player_one_id=player_1_id,
            player_two_id=player_2_id,
        ),
        db=db
    )


@app.post("/tournaments/{tournament_id}/match/{match_id}/result", response_model=schemas.Match)
def result_match(
    tournament_id: UUID,
    match_id: UUID,
    match_result: schemas.MatchUpdate,
    db: Session = Depends(get_db)
) -> schemas.Match:
    db_tournament = read_tournament(tournament_id=tournament_id, db=db)
    if db_tournament.end < D.datetime.now():
        raise HTTPException(status_code=406, detail="Tournament has already ended.")
    elif D.datetime.now() < db_tournament.begin:
        raise HTTPException(status_code=406, detail="Tournament has not started yet.")
    return update_match(
        match_id=match_id,
        match=match_result,
        db=db
    )


@app.get("/tournaments/{tournament_id}/leaderboard")
def leaderboard(tournament_id: UUID, db: Session = Depends(get_db)):
    db_tournament = read_tournament(tournament_id=tournament_id, db=db)
    return db_tournament.leaderboard()
