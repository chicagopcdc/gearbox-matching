import json
from datetime import datetime

from . import logger
from sqlalchemy.orm import Session
from sqlalchemy import select, exc, update
from fastapi import HTTPException
from gearbox.models import Study
from gearbox.schemas import StudyCreate, StudySearchResults, Study as StudySchema
from sqlalchemy.sql.functions import func
from gearbox.util import status, json_utils
from gearbox.crud import study_crud

async def get_study_info(session: Session, id: int) -> StudySchema:
    aes = await study_crud.get_study_info(session, id)
    return aes

async def get_studies_info(session: Session) -> StudySearchResults:
    aes = await study_crud.get_studies_info(session)
    return aes
    pass

async def get_study(session: Session, id: int) -> StudySchema:
    aes = await study_crud.get_study(session, id)
    return aes

async def get_studies(session: Session) -> StudySearchResults:
    aes = await study_crud.get_multi(session)
    return aes

async def create_study(session: Session, study: StudyCreate) -> StudySchema:
    aes = await study_crud.create(db=session, obj_in=study)
    return aes

async def update_study(session: Session, study: StudyCreate, study_id: int) -> StudySchema:
    print("HERE IN UPDATE STUDY SERVICE 1")
    print(f"UPDATE OBJECT ACTIVE: {study['active']}")
    study_in = await study_crud.get(db=session, id=study_id)
    if study_in:
        upd_study = await study_crud.update(db=session, db_obj=study_in, obj_in=study)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study for id: {study_id} not found for update.") 
    print(f"HERE IN UPDATE STUDY SERVICE 2 UPDATED: {upd_study.active}")
    await session.commit() 
    return upd_study

