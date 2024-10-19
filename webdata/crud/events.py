# async crud operations, noted that we focus on operation on database models
# use a baseclass on crud

import uuid

from sqlalchemy import select
from webdata.api import models
from webdata.database import models as db_models
from sqlalchemy.ext.asyncio import AsyncSession



async def crud_create_event(data: models.EventPayload, session: AsyncSession):
    db_event = db_models.Event(**data.model_dump())
    session.add(db_event)
    await session.commit()
    await session.refresh(db_event)
    
    return db_event


# get all events
async def crud_get_events(session: AsyncSession):
    return await session.scalars(select(db_models.Event))

# get user by its id
async def crud_get_event_by_pk(session: AsyncSession, pk: uuid.UUID):
    return await session.get(db_models.Event, pk)

# get user by its id
async def crud_delete_event_by_pk(session: AsyncSession, pk: uuid.UUID):
    # get event by its primary key
    event = await session.get(db_models.Event, pk)
    if event:
        await session.delete(event)
        await session.commit()

    return event
