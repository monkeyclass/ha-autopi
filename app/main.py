from sqlmodel import Session
from typing import Annotated
from fastapi import FastAPI, Depends

from database import create_db_and_tables, engine
from models import EventCreate, Event

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/event/")
def create_hero(event: EventCreate, session: SessionDep) -> dict():
    db_event = Event(
        utc=event.utc,
        cog=event.cog,
        nsat=event.nsat,
        alt=event.alt,
        ts=event.ts,
        t=event.t,
        sog=event.sog,
        lat=event.loc.lat,
        lon=event.loc.lon,
    )

    db_event = Event.model_validate(db_event)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return {}