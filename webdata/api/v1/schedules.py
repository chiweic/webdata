import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webdata.api import models
from webdata.database import models as db_models
from webdata.database.session import get_db_session


router = APIRouter(prefix="/v1", tags=["schedules"])



@router.post("/schedules", status_code=status.HTTP_201_CREATED)
async def create_schedule(
    data: models.SchedulePayload,
    session: AsyncSession = Depends(get_db_session),
) -> models.Schedule:
    schedule = db_models.Schedule(**data.model_dump())
    session.add(schedule)
    await session.commit()
    await session.refresh(schedule)
    return models.Schedule.model_validate(schedule)


@router.get("/schedules", status_code=status.HTTP_200_OK)
async def get_schedules(
    session: AsyncSession = Depends(get_db_session),
) -> list[models.Schedule]:
    schedules = await session.scalars(select(db_models.Schedule))
    return [models.Schedule.model_validate(schedule) for schedule in schedules]


@router.delete("/schedules/{pk}", status_code=status.HTTP_200_OK)
async def delete_schedule(
    pk: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
):
    schedule = await session.get(db_models.Schedule, pk)
    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule does not exist",
        )
    await session.delete(schedule)
    return {'ok': True}


@router.get('/schedules/{pk}', status_code=status.HTTP_200_OK)
async def get_event_by_pk(
    pk: uuid.UUID,
    session: AsyncSession = Depends(get_db_session)
) -> models.Schedule:
    # wait for the database query come back with an event that match
    schedule = await session.get(db_models.Schedule, pk)
    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule does not exist",
        )
    return models.Schedule.model_validate(schedule)