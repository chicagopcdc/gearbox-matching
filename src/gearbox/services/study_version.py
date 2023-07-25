from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import exc, select
from fastapi import HTTPException
from gearbox.models import StudyVersion
from gearbox.schemas import StudyVersionCreate, StudyVersionSearchResults, StudyVersion as StudyVersionSchema, StudyVersionInfo
from sqlalchemy.sql.functions import func
from gearbox.util import status
from gearbox.crud import study_version_crud
from typing import List
from gearbox.util.types import EligibilityCriteriaInfoStatus

async def get_latest_study_version(session: Session, study_id: int) -> int:
    try:
        result = await session.execute(select(func.max(StudyVersion.study_version))
            .where(StudyVersion.study_id == study_id)
        )
        latest_study_version = result.scalar_one()
    except exc.SQLAlchemyError as e:
        logger.error(f"SQL ERROR IN get_latest_study_version method: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

    if latest_study_version:
        return latest_study_version
    else:
        return 0

async def reset_active_status(session: Session, study_id: int) -> bool:
    # set all rows related to the study_version to false
    sae_to_update = await study_version_crud.get_multi(
        db=session, 
        active=True, 
        where=[f"study_version.study_id = {study_id}"]
    )
    for sae in sae_to_update:
        # set all to false
        await study_version_crud.update(db=session, db_obj=sae, obj_in={"active":False})
    return True

async def get_study_version(session: Session, id: int) -> StudyVersionSchema:
    sv = await study_version_crud.get(session, id)
    return sv

async def get_study_versions(session: Session) -> StudyVersionSearchResults:
    sv = await study_version_crud.get_multi(session)
    return sv

async def get_study_versions_by_status(session: Session, study_version_status:str ) -> List[StudyVersionInfo]:

    # check for valid status value 
    if study_version_status not in [item.value for item in EligibilityCriteriaInfoStatus]:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"INVALID STUDY VERSION STATUS: {study_version_status}") 

    sv = await study_version_crud.get_study_versions_by_status(session, study_version_status)
    return sv

async def create_study_version(session: Session, study_version: StudyVersionCreate) -> StudyVersionSchema:

    # find
    study_version.study_version = await get_latest_study_version(session, study_version.study_id) + 1
    # set others to inactive if incoming is active
    if study_version.active:
        reset_active = await reset_active_status(session, study_version.study_id)
    new_study_version = await study_version_crud.create(db=session, obj_in=study_version)

    await session.commit() 
    return new_study_version

async def update_study_version(session: Session, study_version: StudyVersionCreate, study_version_id: int) -> StudyVersionSchema:
    study_version_in = await study_version_crud.get(db=session, id=study_version_id)
    if study_version_in:
        upd_study_version = await study_version_crud.update(db=session, db_obj=study_version_in, obj_in=study_version)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study version for id: {study_version_id} not found for update.") 
    await session.commit() 
    return upd_study_version
