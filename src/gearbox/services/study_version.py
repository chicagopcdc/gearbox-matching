from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import exc, select
from fastapi import HTTPException
from gearbox.models import StudyVersion
from gearbox.schemas import StudyVersionCreate, StudyVersionSearchResults, StudyVersion as StudyVersionSchema, StudyVersionInfo, StudyVersionUpdate
from sqlalchemy.sql.functions import func
from gearbox.util import status
from gearbox.crud import study_version_crud
from typing import List
from gearbox.util.types import StudyVersionStatus

async def get_latest_study_version(session: Session, study_id: int) -> int:
    try:
        result = await session.execute(select(func.max(StudyVersion.study_version_num))
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
    sv_to_update = await study_version_crud.get_multi(
        db=session, 
        where=[f"{StudyVersion.__table__.name}.study_id = {study_id} AND {StudyVersion.__table__.name}.status = '{StudyVersionStatus.ACTIVE.value}'"]
    )
    for sv in sv_to_update:
        await study_version_crud.update(db=session, db_obj=sv, obj_in={"status":StudyVersionStatus.INACTIVE})
    return True

async def get_study_version(session: Session, id: int) -> StudyVersionSchema:
    sv = await study_version_crud.get(session, id)
    return sv

async def get_study_versions(session: Session) -> StudyVersionSearchResults:
    sv = await study_version_crud.get_multi(session)
    return sv

async def get_study_versions_for_adjudication(session: Session) -> List[StudyVersionInfo]:
    sv = await study_version_crud.get_study_versions_for_adjudication(session)
    return sv

async def get_study_versions_by_status(session: Session, study_version_status:StudyVersionStatus ) -> List[StudyVersionInfo]:

    sv = await study_version_crud.get_multi(
        db=session, 
        where=[f"{StudyVersion.__table__.name}.status = '{study_version_status}'"]
    )
    return sv

async def create_study_version(session: Session, study_version: StudyVersionCreate ) -> StudyVersionSchema:

    # find
    study_version.study_version_num = await get_latest_study_version(session, study_version.study_id) + 1

    # set others to inactive if incoming is active
    if study_version.status == StudyVersionStatus.ACTIVE:
        reset_active = await reset_active_status(session, study_version.study_id)
    new_study_version = await study_version_crud.create(db=session, obj_in=study_version)

    # await session.commit() 
    return new_study_version

async def update_study_version(session: Session, study_version: StudyVersionUpdate) -> StudyVersionSchema:
    study_version_in = await study_version_crud.get(db=session, id=study_version.id)
    if study_version_in:
        upd_study_version = await study_version_crud.update(db=session, db_obj=study_version_in, obj_in=study_version)
    else:
        logger.error(f"Study version for id: {study_version.id} not found for update.") 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study version for id: {study_version.id} not found for update.") 
    await session.commit() 
    return upd_study_version