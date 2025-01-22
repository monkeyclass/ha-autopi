import uuid

from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

class Location(SQLModel):
    lat: float
    lon: float

class EventBase(SQLModel):
    utc: str = Field(index=True)
    cog: float
    nsat: int
    alt: int
    ts: str
    t: str
    sog: int

class EventCreate(EventBase):
    loc: Location

class Event(EventBase, Location, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

