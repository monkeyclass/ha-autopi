from fastapi import FastAPI
from sqlmodel import Session

from database import create_db_and_tables, engine
from models import EventCreate, Event

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/event/")
def create_hero(event: EventCreate):
    with Session(engine) as session:
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
        return db_event