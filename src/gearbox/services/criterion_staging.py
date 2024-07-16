from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession as Session
from . import logger
from gearbox.util import status
from gearbox.schemas import CriterionStaging as CriterionStagingSchema, CriterionStagingCreate, CriterionStagingSearchResults
from gearbox.crud import criterion_staging_crud, criterion_has_value_crud, criterion_has_tag_crud, display_rules_crud, triggered_by_crud, value_crud, tag_crud

async def get_criterion_staging(session: Session, id: int) -> CriterionStagingSchema:
    crit = await criterion_staging_crud.get(session, id)
    return crit

async def get_criteria_staging(session: Session) -> CriterionStagingSearchResults:
    aes = await criterion_staging_crud.get_multi(session)
    return aes

# async def get_criteria_staging_by_id


async def create(session: Session, staging_criterion: CriterionStagingCreate)-> CriterionStagingSchema:
    # TO DO? - check code exists in the criterion table?

    new_staging_criterion = await criterion_staging_crud.create(db=session, obj_in=staging_criterion)
    return new_staging_criterion

"""
async def update_criterion(session: Session, criterion: CriterionCreateIn, criterion_id: int) -> CriterionSchema:
    criterion_to_upd = await criterion_staging_crud.get(db=session, id=criterion_id)

    if criterion_to_upd:
        upd_criterion = await criterion_staging_crud.update(db=session, db_obj=criterion_to_upd, obj_in=criterion)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Criterion id: {criterion_id} not found for update.") 
    await session.commit() 

    return upd_criterion
"""