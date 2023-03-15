from gearbox.crud import eligibility_criteria_info_crud
from gearbox.schemas import EligibilityCriteriaInfoCreate, EligibilityCriteriaInfoSearchResults, EligibilityCriteriaInfo as EligibilityCriteriaInfoSchema
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import HTTPException
from gearbox.util import status

async def reset_active_status(session: Session, study_version_id: int) -> bool:
    # set all rows related to the study_version to false
    sae_to_update = await eligibility_criteria_info_crud.get_multi(
        db=session, 
        active=True, 
        where=[f"eligibility_criteria_info.study_version_id = {study_version_id}"]
    )
    for sae in sae_to_update:
        # set all to false
        await eligibility_criteria_info_crud.update(db=session, db_obj=sae, obj_in={"active":False})
    return True

async def get_eligibility_criteria(session: Session, id: int) -> EligibilityCriteriaInfoSchema:
    ec = await eligibility_criteria_info_crud.get(session, id)
    return ec

async def get_eligibility_criteria(session: Session) -> EligibilityCriteriaInfoSearchResults: 
    ecs = await eligibility_criteria_info_crud.get_multi(session)
    return ecs
    pass

async def create_eligibility_criteria(session: Session, eligibility_criteria_info: EligibilityCriteriaInfoCreate) -> EligibilityCriteriaInfoSchema:
    new_eligibility_criteria_info = await eligibility_criteria_info.create(db=session, obj_in=eligibility_criteria_info)
    await session.commit() 
    return new_eligibility_criteria_info

async def update_eligibility_criteria(session: Session, eligibility_criteria_info: EligibilityCriteriaInfoCreate, eligibility_criteria_info_id: int) -> EligibilityCriteriaInfoSchema:
    eligibility_criteria_info_in = await eligibility_criteria_info_crud.get(db=session, id=eligibility_criteria_info_id)
    if eligibility_criteria_info_in:
        upd_eligibility_criteria_info = await eligibility_criteria_info_crud.update(db=session, db_obj=eligibility_criteria_info_in, obj_in=eligibility_criteria_info)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Eligibility_criteria id: {eligibility_criteria_info_id} not found for update.") 
    await session.commit() 
    return upd_eligibility_criteria_info