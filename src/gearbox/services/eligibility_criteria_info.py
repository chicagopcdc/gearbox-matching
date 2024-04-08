from gearbox.crud import eligibility_criteria_info_crud, study_version_crud, eligibility_criteria_crud, study_algorithm_engine_crud
from gearbox.schemas import EligibilityCriteriaInfoCreate, EligibilityCriteriaInfoSearchResults, EligibilityCriteriaInfo as EligibilityCriteriaInfoSchema
from gearbox.models import EligibilityCriteriaInfo
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import HTTPException
from gearbox.util import status
from gearbox.util.types import EligibilityCriteriaInfoStatus

async def reset_active_status(session: Session, study_version_id: int) -> bool:

    # set all currently active rows related to the study_version to inactive
    eci_to_update = await eligibility_criteria_info_crud.get_multi(
        db=session,
        where=[f"eligibility_criteria_info.study_version_id = {study_version_id} and eligibility_criteria_info.status = '{EligibilityCriteriaInfoStatus.ACTIVE.value}'"],
        noload_rel = [EligibilityCriteriaInfo.study_version]
    )
    for eci in eci_to_update:
        # set all to false
        await eligibility_criteria_info_crud.update(db=session, db_obj=eci, obj_in={"status":EligibilityCriteriaInfoStatus.INACTIVE.value})
    return True

async def get_eligibility_criteria_info(session: Session, id: int) -> EligibilityCriteriaInfoSchema:
    ec = await eligibility_criteria_info_crud.get(session, id)
    return ec

async def get_eligibility_criteria_infos(session: Session) -> EligibilityCriteriaInfoSearchResults: 
    ecs = await eligibility_criteria_info_crud.get_multi(session)
    return ecs
    pass

async def create_eligibility_criteria_info(session: Session, eligibility_criteria_info: EligibilityCriteriaInfoCreate) -> EligibilityCriteriaInfoSchema:

    # validate all fks in input
    check_id_errors = []
    check_id_errors.append(await study_version_crud.check_key(db=session, ids_to_check=eligibility_criteria_info.study_version_id))
    check_id_errors.append(await study_algorithm_engine_crud.check_key(db=session, ids_to_check=eligibility_criteria_info.study_algorithm_engine_id))
    check_id_errors.append(await eligibility_criteria_crud.check_key(db=session, ids_to_check=eligibility_criteria_info.eligibility_criteria_id))


    if not all(i is None for i in check_id_errors):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR: missing FKs for eligibility_criteria_info creation: {[error for error in check_id_errors if error]}")        


    # if incoming info is active, then reset any currently active infos for the study_version 
    if eligibility_criteria_info.status.value == EligibilityCriteriaInfoStatus.ACTIVE.value:
        retval = await reset_active_status(session=session, study_version_id=eligibility_criteria_info.study_version_id)

    new_eligibility_criteria_info = await eligibility_criteria_info_crud.create(db=session, obj_in=eligibility_criteria_info)
    await session.commit() 
    return new_eligibility_criteria_info

async def update_eligibility_criteria_info(session: Session, eligibility_criteria_info: EligibilityCriteriaInfoCreate, eligibility_criteria_info_id: int) -> EligibilityCriteriaInfoSchema:
    eligibility_criteria_info_to_upd = await eligibility_criteria_info_crud.get(db=session, id=eligibility_criteria_info_id)
    # if updating status to active, then set status to inactive for any 
    # currently active eligibility_criteria_info rows for the study version
    if 'status' in eligibility_criteria_info.keys() and eligibility_criteria_info['status'] == EligibilityCriteriaInfoStatus.ACTIVE.value:
            reset_active_status(session=session, study_version_id=eligibility_criteria_info_to_upd.study_version_id)

    if eligibility_criteria_info_to_upd:
        upd_eligibility_criteria_info = await eligibility_criteria_info_crud.update(db=session, db_obj=eligibility_criteria_info_to_upd, obj_in=eligibility_criteria_info)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Eligibility_criteria id: {eligibility_criteria_info_id} not found for update.") 
    await session.commit() 

    return upd_eligibility_criteria_info