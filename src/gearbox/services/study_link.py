import json
from datetime import datetime

from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import exc
from fastapi import HTTPException
from gearbox.models import StudyLink
from gearbox.schemas import StudyLinkCreate, StudyLinkSearchResults, StudyLink as StudyLinkSchema
from gearbox.util import status, json_utils
from gearbox.crud import study_link_crud

async def get_study_link(session: Session, id: int) -> StudyLinkSchema:
    aes = await study_link_crud.get(session, id)
    return aes

async def get_study_links(session: Session) -> StudyLinkSearchResults:
    aes = await study_link_crud.get_multi(session)
    return aes
    pass

async def create_study_link(session: Session, study_link: StudyLinkCreate) -> StudyLinkSchema:

    new_study_link = await study_link_crud.create(db=session, obj_in=study_link)
    return new_study_link

async def update_study_link(session: Session, study_link: StudyLinkCreate, study_link_id: int): 
    study_link_in = await study_link_crud.get(db=session, id=study_link_id)
    if study_link_in:
        upd_study_link = await study_link_crud.update(db=session, db_obj=study_link_in, obj_in=study_link)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study link for id: {study_link_id} not found for update.") 