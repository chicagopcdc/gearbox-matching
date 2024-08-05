from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession as Session
from . import logger
from gearbox.util import status
from gearbox.schemas import CriterionStaging as CriterionStagingSchema, CriterionStagingCreate
from gearbox.crud import criterion_staging_crud, criterion_has_value_crud, criterion_has_tag_crud, display_rules_crud, triggered_by_crud, value_crud, tag_crud
from typing import List

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
    # TO DO? - check code exists in the criterion table?

    new_staging_criterion = await criterion_staging_crud.create(db=session, obj_in=staging_criterion)
    return new_staging_criterion

async def update(session: Session, criterion: CriterionStagingSchema) -> CriterionStagingSchema:
    criterion_to_upd = await criterion_staging_crud.get(db=session, id=criterion.id)

    ## save the user-id of the user making the update

    if criterion_to_upd:
        upd_criterion = await criterion_staging_crud.update(db=session, db_obj=criterion_to_upd, obj_in=criterion)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Criterion id: {criterion.id} not found for update.") 
    await session.commit() 

    return upd_criterion