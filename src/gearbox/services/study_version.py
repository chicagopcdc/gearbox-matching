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
from gearbox.util.types import StudyVersionStatus, AdjudicationStatus, EchcAdjudicationStatus
from gearbox.services import criterion_staging as criterion_staging_service

async def get_latest_study_version(session: Session, study_id: int) -> int:

    latest_study_version = await study_version_crud.get_latest_study_version(current_session=session, study_id=study_id)
    if latest_study_version:
        return latest_study_version.study_version_num
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


async def publish_study_version(session: Session, study_version_id: int):
    # check if study_version is valid for publishing? is there 
    # an existing 'ACTIVE' study_version for the given study?

    # get eligibility_criteria_id
    study_version = await study_version_crud.get(db=session, id=study_version_id)
    if not study_version:
        logger.error(f"Study version for id: {study_version_id} not found for publishing.") 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study version for id: {study_version.id} not found for update.") 

    # Check for existing ACTIVE study_versions for the study
    existing_active_svs = await study_version_crud.get_multi(session, 
        where=[f"{StudyVersion.__table__.name}.study_id = {study_version.study_id} and {StudyVersion.__table__.name}.status = '{StudyVersionStatus.ACTIVE.value}'"])
    qc_errors = []
    if existing_active_svs:
        qc_errors.append(f"Existing ACTIVE study_versions found ids: {[x.id for x in existing_active_svs]}")

    # ===> CAN ALL OF THE FOLLOWING QCs BE DONE TOGETHER BEFORE THROWING EXCEPTION? 
    # check all rows in criterion_staging are 'ACTIVE' or 'INACTIVE' criterion_adjudication_status
    invalid_status = list(set([x for x in AdjudicationStatus]) - set([AdjudicationStatus.ACTIVE, AdjudicationStatus.INACTIVE]))
    invalid_criterion_adjudication = await criterion_staging_service.get_criterion_staging_by_criterion_adjudication_status(
        session=session, 
        eligibility_criteria_id=study_version.eligibility_criteria_id, 
        adjudication_status = invalid_status
    )
    if invalid_criterion_adjudication:
        qc_errors.append(f"The following criteria require final adjudication: {[x.id for x in invalid_criterion_adjudication ]}")

    # check criterion_id exists for all the above
    staging_missing_criterion = await criterion_staging_service.get_criterion_staging_missing_criterion_id(session=session, eligibility_criteria_id=study_version.eligibility_criteria_id)
    qc_errors.append(f"The following criterion_staging ids are missing criterion ids: {[x.id for x in staging_missing_criterion]}")

    # TO DO: check all criterion_ids in criterion_staging are for ACTIVE criterions...
    staging_inactive_criterion = await criterion_staging_service.get_criterion_staging_inactive_criterion(session=session, eligibility_criteria_id=study_version.eligibility_criteria_id)

    # check all rows in criterion_staging are 'ACTIVE' or 'INACTIVE' echc_adjudication_status
    invalid_echc_adjudication = await criterion_staging_service.get_criterion_staging_by_echc_criterion_adjudication_status(
        session=session, 
        eligibility_criteria_id=study_version.eligibility_criteria_id,
        echc_adjudication_status=[EchcAdjudicationStatus.NEW, EchcAdjudicationStatus.IN_PROCESS] 
    )
    # check value row exists for each of the above
    # TO DO: check study_alogrithm_logic exists and all echc exist in the logic json
    # modify study_version.status to ACTIVE - and modify study.active to 'True'

    # if any errors found
    if qc_errors:
        logger.error(f"{qc_errors}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{qc_errors}")
