# this will capture all routes for events
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webdata.api import models
from webdata.database import models as db_models
from webdata.database.session import get_db_session


router = APIRouter(prefix="/v1", tags=["sections"])


# this will create section with event infomations
@router.post("/sections", status_code=status.HTTP_201_CREATED)
async def create_section(
    data: models.SectionPayload,
    session: AsyncSession = Depends(get_db_session),
) -> models.Section:
    # example of incoming data
    data_dict = data.model_dump()
    events = await session.scalars(
        select(db_models.Event).where(
            db_models.Event.pk.in_(data_dict.pop("events"))
        )
    )
    section = db_models.Section(**data_dict, events=list(events))
    session.add(section)
    await session.commit()
    await session.refresh(section)
    return models.Section.model_validate(section)


@router.get("/sections", status_code=status.HTTP_200_OK)
async def get_sections(
    session: AsyncSession = Depends(get_db_session),
) -> list[models.Section]:
    sections = await session.scalars(select(db_models.Section))
    return [models.Section.model_validate(section) for section in sections]


@router.delete("/sections/{pk}", status_code=status.HTTP_200_OK)
async def delete_section(
    pk: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
):
    section = await session.get(db_models.Section, pk)
    if section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section does not exist",
        )
    await session.delete(section)
    return {'ok': True}


