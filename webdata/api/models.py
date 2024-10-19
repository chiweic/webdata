from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime, timezone

class Ingredient(BaseModel):
    """Ingredient model."""

    model_config = ConfigDict(from_attributes=True)

    pk: UUID
    name: str


class IngredientPayload(BaseModel):
    """Ingredient payload model."""

    name: str = Field(min_length=1, max_length=127)


class Potion(BaseModel):
    """Potion model."""

    model_config = ConfigDict(from_attributes=True)

    pk: UUID
    name: str
    ingredients: list[Ingredient]


class PotionPayload(BaseModel):
    """Potion payload model."""

    name: str = Field(min_length=1, max_length=127)
    ingredients: list[UUID] = Field(min_length=1)


# the definitions on pydantic models used on api
# purpose is to validate (instance creation)

# we declare the base model must contain the following fields
# pk: key that identified each object
# model_config: this kind of define model behaviors
# created: timestamp on creation
# updated: when last time it get accessed (in stead of modified)

# Base model conained pure parameters
# all models on actual operations will inherit this
# mininum will place Optional/List on the parameters
# field is used for description and alias

from datetime import date, time
# this is the factory functon timestamp get generated
def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class EvantBase(BaseModel):
    """The Base model for Event"""
    start_time: time
    end_time: time
    event_date: date
    location: str


# This is the 'full' model, with pk (primary key etc.,)
# The default behavior of Pydantic is to validate the data when the model is created.
# In case the user changes the data after the model is created, the model is not revalidated, set to True

class Event(EvantBase):
    """Event model"""
    model_config = ConfigDict(from_attributes=True)
    pk: UUID = Field(default_factory=uuid4)                         # this will be generated at the pydantic side, not database
    

# this is the class when we try to create an event
# that from api, only parameters thaat are "MUST" included will be here
# we assumed the return from api call will jusr return the 'full' class
# while app will use model_dump to set fields of interest
# the point of not directly use the EventBase, would be NOT exposing name to api/routes
# or you would use extra field only in parameter but not in mapping
class EventPayload(EvantBase):
    """Event Payload model"""
    created: Optional[datetime] = Field(default=None)               # this get only used in path operation, not mapping
    

class SectionBase(BaseModel):
    title: str
    status: Optional[str] 
    events: list[Event]

class Section(SectionBase):
    """Section model."""
    model_config = ConfigDict(from_attributes=True)
    pk: UUID
    

class SectionPayload(SectionBase):
    """Section payload model."""
    pass


class ScheduleBase(BaseModel):
    # url, title, descriptions, venues:json, registrations:json
    # sections: list...
    url: str
    title: str
    description: str
    venue: str
    registration: dict
    location: dict
    sections: list[Section]

class Schedule(ScheduleBase):
    """Schedule base model"""
    model_config = ConfigDict(from_attributes=True)
    pk: UUID


class SchedulePayload(ScheduleBase):
    """Schedule base model"""
    pass