import os

from sqlmodel import Session
from typing import Annotated
from starlette import status
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database import create_db_and_tables, engine
from models import EventCreate, Event

app = FastAPI()
security = HTTPBearer()
load_dotenv()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

auth_token = os.getenv("AUTH_TOKEN")

async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

@app.post("/event/")
def create_event(
    event: EventCreate,
    session: SessionDep,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(validate_token)]
) -> dict():
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