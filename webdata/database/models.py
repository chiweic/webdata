from typing import Annotated, Optional
import uuid
from datetime import time, date
import datetime
from sqlalchemy import TIMESTAMP, Column, DateTime, ForeignKey, Table, func, orm
from sqlalchemy.dialects.postgresql import UUID

class Base(orm.DeclarativeBase):
    """Base database model."""

    pk: orm.Mapped[uuid.UUID] = orm.mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    
potion_ingredient_association = Table(
    "potion_ingredient",
    Base.metadata,
    Column("potion_id", UUID(as_uuid=True), ForeignKey("potion.pk")),
    Column("ingredient_id", UUID(as_uuid=True), ForeignKey("ingredient.pk")),
)

section_event_association = Table(
    'section_event',
    Base.metadata,
    Column("section_id", UUID(as_uuid=True), ForeignKey("sections.pk")),
    Column("event_id", UUID(as_uuid=True), ForeignKey("events.pk")),
)

schedule_section_association = Table(
    'schedule_section',
    Base.metadata,
    Column("schedule_id", UUID(as_uuid=True), ForeignKey("schedules.pk")),
    Column("section_id", UUID(as_uuid=True), ForeignKey("sections.pk")),
)


class Ingredient(Base):
    """Ingredient database model."""

    __tablename__ = "ingredient"

    name: orm.Mapped[str]
    

class Potion(Base):
    """Potion database model."""

    __tablename__ = "potion"

    name: orm.Mapped[str]
    ingredients: orm.Mapped[list["Ingredient"]] = orm.relationship(
        secondary=potion_ingredient_association,
        backref="potions",
        lazy="selectin",
    )


# sqlalchemy timestamp example: see https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
timestamp = Annotated[
    datetime.datetime,
    orm.mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]

class Event(Base):
    """Event database model"""

    __tablename__ = 'events'

    event_date: orm.Mapped[date]
    start_time: orm.Mapped[time]
    end_time : orm.Mapped[time]
    location : orm.Mapped[str]
    # timestamped are marked at database side
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    

class Section(Base):
    """Section database model"""

    __tablename__ = 'sections'

    title: orm.Mapped[str]
    status: orm.Mapped[str] = orm.mapped_column(default=None, nullable=True)

    events: orm.Mapped[list['Event']] = orm.relationship(
        secondary=section_event_association,
        backref='sections',
        lazy='selectin'
    )

from sqlalchemy import JSON
class Schedule(Base):
    """Schedule Base model"""

    __tablename__ = 'schedules'

    title: orm.Mapped[str] = orm.mapped_column(default=None, nullable=False)
    url: orm.Mapped[str] = orm.mapped_column(default=None, nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(default=None, nullable=False)
    venue: orm.Mapped[str] = orm.mapped_column(default=None, nullable=False)
    registration: orm.Mapped[dict] = orm.mapped_column(JSON, nullable=False)  # JSON field using orm.Mapped
    location: orm.Mapped[dict] = orm.mapped_column(JSON, nullable=False)  # JSON field using orm.Mapped

    sections: orm.Mapped[list['Section']] = orm.relationship(
        secondary=schedule_section_association,
        backref='schedules',
        lazy='selectin'
    )