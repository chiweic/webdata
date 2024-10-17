import uuid
from datetime import time
from pydantic import BaseModel, ConfigDict, Field


class Ingredient(BaseModel):
    """Ingredient model."""

    model_config = ConfigDict(from_attributes=True)

    pk: uuid.UUID
    name: str


class IngredientPayload(BaseModel):
    """Ingredient payload model."""

    name: str = Field(min_length=1, max_length=127)


class Potion(BaseModel):
    """Potion model."""

    model_config = ConfigDict(from_attributes=True)

    pk: uuid.UUID
    name: str
    ingredients: list[Ingredient]


class PotionPayload(BaseModel):
    """Potion payload model."""

    name: str = Field(min_length=1, max_length=127)
    ingredients: list[uuid.UUID] = Field(min_length=1)


class Event(BaseModel):
    """Event model"""

    model_config = ConfigDict(from_attributes=True)
    pk: uuid.UUID
    start_time: time
    end_time: time
    location: str


class EventPayload(BaseModel):
    """Event Payload model"""

    start_time: time = Field(default=None)
    end_time: time = Field(default=None)
    location: str = Field(min_length=1, max_length=127)
