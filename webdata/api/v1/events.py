# this will capture all routes for events
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webdata.api import models
from webdata.database.session import get_db_session

from webdata.crud.events import crud_create_event, crud_delete_event_by_pk, crud_get_events, crud_get_event_by_pk

router = APIRouter(prefix="/v1", tags=["events"])


@router.post("/events", status_code=status.HTTP_201_CREATED)
async def create_event(
    data: models.EventPayload,
    session: AsyncSession = Depends(get_db_session),
) -> models.Event:
    
    # leave the pydantic model to db model to crud operations
    event = await crud_create_event(data=data, session=session)
    # we should just leave with pure pydantic models
    return models.Event.model_validate(event)


@router.get('/events/{pk}', status_code=status.HTTP_200_OK)
async def get_event_by_pk(
    pk: uuid.UUID,
    session: AsyncSession = Depends(get_db_session)
) -> models.Event:
    # wait for the database query come back with an event that match
    event = await crud_get_event_by_pk(session=session, pk=pk)
    # instansiate if we have an record
    if event:
        return models.Event.model_validate(event)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='cannot find event'
        )


@router.get("/events", status_code=status.HTTP_200_OK)
async def get_events(
    session: AsyncSession = Depends(get_db_session),
) -> list[models.Event]:
    events = await crud_get_events(session=session)
    return [models.Event.model_validate(event) for event in events]


@router.delete("/events/{pk}", status_code=status.HTTP_200_OK)
async def delete_event(
    pk: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> models.Event:
    event = await crud_delete_event_by_pk(session=session, pk=pk)
    if event:
        return models.Event.model_validate(event)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='cannot find event'
        )
    


    #        raise HTTPException(
    #        status_code=status.HTTP_404_NOT_FOUND,
    #        detail="Ingredient does not exist")
    #    
