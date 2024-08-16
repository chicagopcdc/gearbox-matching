from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as Session
from gearbox.util import status
from gearbox.schemas import CriterionStaging as CriterionStagingSchema, CriterionStagingCreate, CriterionPublish, CriterionCreate, CriterionStagingUpdate, CriterionHasValueCreate
from gearbox.crud import criterion_staging_crud , study_version_crud, value_crud, criterion_has_value_crud, input_type_crud
from typing import List
from gearbox.util.types import StudyVersionStatus, AdjudicationStatus
from gearbox.services import criterion as criterion_service
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

async def publish_criterion(session: Session, criterion: CriterionPublish, user_id: int):

    # qc values
    check_id_errors = []
    if criterion.values:
        check_id_errors.append(await value_crud.check_key(db=session, ids_to_check=criterion.values))
        if not all(i is None for i in check_id_errors):
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR PUBLISHING CRITERION: missing FKs for criterion creation: {[error for error in check_id_errors if error]}")        

        # qc input_type: check that input_type.data_type is list for the input_type_id
        input_type = await input_type_crud.get(db=session, id=criterion.input_type_id)
        # only 'list' input-types can have criterion_has_value rows
        if input_type.data_type != "list":
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR PUBLISHING CRITERION: {input_type.data_type} can not have associated values.") 


    # Convert criterion to CriterionCreate
    criterion_save=CriterionCreate(**criterion.dict())
    new_criterion = await criterion_service.save_criterion(session=session, criterion=criterion_save)

    # Create criterion has values here
    if criterion.values:
        for v_id in criterion.values:
            chv = CriterionHasValueCreate(criterion_id=new_criterion.id, value_id=v_id)
            await criterion_has_value_crud.create(db=session,obj_in=chv)

    # Call update method below - set criterion_staging criteria adjudication status to active
    stage_upd = CriterionStagingUpdate(id=criterion.criterion_staging_id, criterion_id=new_criterion.id, criterion_adjudication_status=AdjudicationStatus.ACTIVE)
    update(session=session, criterion=stage_upd, user_id=user_id)

async def update(session: Session, criterion: CriterionStagingUpdate, user_id: int ) -> CriterionStagingSchema:

    criterion_to_upd = await criterion_staging_crud.get(db=session, id=criterion.id)
    study_version_to_upd = await study_version_crud.get_study_version_ec_id(current_session=session, eligibility_criteria_id = criterion_to_upd.eligibility_criteria_id )
    sv = await study_version_crud.update(db=session, db_obj=study_version_to_upd, obj_in={"status": StudyVersionStatus.IN_PROCESS})

    criterion_in_dict = dict(criterion)
    to_upd_dict = criterion_to_upd.__dict__
    updates=[]

    # Track any updates besides status updates for logging
    for key in criterion_in_dict:
        if criterion_in_dict.get(key) and criterion_in_dict.get(key) != to_upd_dict.get(key) and "status" not in key:
            updates.append(f'criterion_staging update:  {key} changed from {criterion_in_dict.get(key)} to {to_upd_dict.get(key)}')

    if criterion_to_upd:
        criterion.last_updated_by_user_id = user_id
        upd_criterion = await criterion_staging_crud.update(db=session, db_obj=criterion_to_upd, obj_in=criterion)
    else:
        logger.error(f"Criterion id: {criterion.id} not found for update.") 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Criterion id: {criterion.id} not found for update.") 
    await session.commit() 
    if updates:
        logger.info(f"Criterion staging id: {criterion_to_upd.id} updated by user_id: {user_id} updates include: {updates}")

    return upd_criterion