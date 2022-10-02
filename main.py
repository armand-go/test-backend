from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import engine, SessionLocal
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
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered."
        )
    return crud.create_user(db=db, user=user)


# TODO: Implement pagination and filter
@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    users = crud.get_users(db, skip, limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@app.put("/users/update/{user_id}", response_model=schemas.User)
def update_user(user_id: UUID, user: schemas.UserUpdate, db: Session = Depends(get_db)):
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
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    return crud.create_match(db=db, match=match)


@app.get("/matches/{match_id}", response_model=schemas.Match)
def read_match(match_id: UUID, db: Session = Depends(get_db)):
    match = crud.get_match(db, match_id=match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found.")
    return match


@app.put("/matches/update/{match_id}", response_model=schemas.Match)
def update_match(match_id: UUID, match: schemas.MatchUpdate, db: Session = Depends(get_db)):
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
def create_tournament(tournament: schemas.TournamentCreateUpdate, db: Session = Depends(get_db)):
    return crud.create_tournament(db=db, tournament=tournament)


@app.get("/tournaments/", response_model=list[schemas.Tournament])
def read_tournaments(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    tournaments = crud.get_tournaments(db, skip, limit)
    return tournaments


@app.get("/tournaments/{tournament_id}", response_model=schemas.Tournament)
def read_tournament(tournament_id: UUID, db: Session = Depends(get_db)):
    tournament = crud.get_tournament(db, tournament_id=tournament_id)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found.")
    return tournament


@app.put("/tournaments/update/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_tournament(
    tournament_id: UUID,
    tournament: schemas.TournamentCreateUpdate,
    db: Session = Depends(get_db)
):
    db_tournament = crud.get_tournament(db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found.")
    return crud.update_tournament(db, db_tournament, tournament)


@app.delete("/tournaments/delete/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tournament(tournament_id: UUID, db: Session = Depends(get_db)):
    db_tournament = crud.get_tournament(db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Match not found.")
    return crud.delete_tournament(db, db_tournament)
