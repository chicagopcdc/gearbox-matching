from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as Session
from gearbox.util import status
from gearbox.schemas import CriterionStaging as CriterionStagingSchema, CriterionStagingCreate
from gearbox.crud import criterion_staging_crud , study_version_crud
from typing import List
from gearbox.util.types import StudyVersionStatus
from . import logger

async def get_criterion_staging(session: Session, id: int) -> CriterionStagingSchema:
    crit = await criterion_staging_crud.get(session, id)
    return crit

async def get_criteria_staging(session: Session) -> List[CriterionStagingSchema]:
    cs = await criterion_staging_crud.get_multi(session)
    return cs

async def get_criterion_staging_by_ec_id(session: Session, eligibility_criteria_id: int) -> List[CriterionStagingSchema]:
    cs = await criterion_staging_crud.get_criterion_staging_by_ec_id(session, eligibility_criteria_id)
    return cs

async def create(session: Session, staging_criterion: CriterionStagingCreate)-> CriterionStagingSchema:

    new_staging_criterion = await criterion_staging_crud.create(db=session, obj_in=staging_criterion)
    return new_staging_criterion

async def update(session: Session, criterion: CriterionStagingSchema, user_id: int) -> CriterionStagingSchema:

    criterion_to_upd = await criterion_staging_crud.get(db=session, id=criterion.id)
    study_version_to_upd = await study_version_crud.get_study_version_ec_id(current_session=session, eligibility_criteria_id = criterion_to_upd.eligibility_criteria_id )
    sv = await study_version_crud.update(db=session, db_obj=study_version_to_upd, obj_in={"status": StudyVersionStatus.IN_PROCESS})

    if criterion_to_upd:
        criterion_to_upd.last_updated_by = user_id
        upd_criterion = await criterion_staging_crud.update(db=session, db_obj=criterion_to_upd, obj_in=criterion)
    else:
        logger.error(f"Criterion id: {criterion.id} not found for update.") 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Criterion id: {criterion.id} not found for update.") 
    await session.commit() 
    logger.info(f"Criterion staging id: {criterion_to_upd.id} updated by: {user_id}")

    return upd_criterion