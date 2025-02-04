from . import logger
from gearbox.crud import el_criteria_has_criterion_crud, study_version_crud, eligibility_criteria_crud, value_crud, criterion_crud, criterion_staging_crud
from gearbox.schemas import ElCriteriaHasCriterionCreate, ElCriteriaHasCriterionSearchResults, ElCriteriaHasCriterion as ElCriteriaHasCriterionSchema, ElCriteriaHasCriterionPublish, CriterionStagingUpdate
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import HTTPException
from gearbox.util import status
from gearbox.models import ElCriteriaHasCriterion
from gearbox.services import criterion_staging as criterion_staging_service
from gearbox.util.types import StudyVersionStatus, AdjudicationStatus, EchcAdjudicationStatus
from gearbox import auth

async def get_el_criteria_has_criterion(session: Session, id: int) -> ElCriteriaHasCriterionSchema:
    ec = await el_criteria_has_criterion_crud.get(session, id)
    return ec

async def get_el_criteria_has_criterions(session: Session) -> ElCriteriaHasCriterionSearchResults: 
    ecs = await el_criteria_has_criterion_crud.get_multi(session)
    return ecs

async def get_el_criteria_has_criterions_by_ecid(session: Session, ecid: int) -> ElCriteriaHasCriterionSearchResults: 
    ecs = await el_criteria_has_criterion_crud.get_multi(session, where=[f"eligibility_criteria_id = {ecid}"])
    return ecs

async def create_el_criteria_has_criterion(session: Session, el_criteria_has_criterion: ElCriteriaHasCriterionCreate) -> ElCriteriaHasCriterion:
    new_echc = await el_criteria_has_criterion_crud.create(db=session, obj_in=el_criteria_has_criterion)
    # What about questions that appear 2 or more times in a study with different values? (Yes/No nested for example)
    constraint_cols = [ElCriteriaHasCriterion.criterion_id, ElCriteriaHasCriterion.eligibility_criteria_id]
    """
    no_update_cols = ['create_date']
            constraint_cols = [Study.code]
            new_or_updated_study_id = await study_crud.upsert(
                db=session,
                model=Study, 
                row=row, 
                as_of_date_col='create_date',
                no_update_cols=no_update_cols,
                constraint_cols=constraint_cols
    """
    return new_echc

async def update_el_criteria_has_criterion(session: Session, el_criteria_has_criterion: ElCriteriaHasCriterionCreate, el_criteria_has_criterion_id: int) -> ElCriteriaHasCriterionSchema:
    el_criteria_has_criterion_in = await el_criteria_has_criterion_crud.get(db=session, id=el_criteria_has_criterion_id)
    if el_criteria_has_criterion_in:
        upd_el_criteria_has_criterion = await el_criteria_has_criterion_crud.update(db=session, db_obj=el_criteria_has_criterion_in, obj_in=el_criteria_has_criterion)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"el_criteria_has_criterion id: {el_criteria_has_criterion_id} not found for update.") 
    await session.commit() 
    return upd_el_criteria_has_criterion

async def publish_echc(session: Session, echc: ElCriteriaHasCriterionPublish, user_id: int) -> ElCriteriaHasCriterion:

    check_id_errors = []

    existing_staging = await criterion_staging_service.get_criterion_staging(session=session, id=echc.criterion_staging_id)

    # criterion (question) must be in ACTIVE or EXISTING status before we can assign a value to the study criteria
    if existing_staging.criterion_adjudication_status not in (AdjudicationStatus.ACTIVE, AdjudicationStatus.EXISTING):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 
            f"Criterion staging id: {echc.criterion_staging_id} status must be active in order to publish el_criteria_has_criterion. The current status is: {existing_staging.criterion_adjudication_status} - finalize criterion adjudication before publishing.")

    # Check ids exist for value, eligibility_criteria, criterion
    check_id_errors.append(await value_crud.check_key(db=session, ids_to_check=echc.value_ids))
    check_id_errors.append(await eligibility_criteria_crud.check_key(db=session, ids_to_check=echc.eligibility_criteria_id))
    check_id_errors.append(await criterion_crud.check_key(db=session, ids_to_check=echc.criterion_id))
    check_id_errors.append(await criterion_staging_crud.check_key(db=session, ids_to_check=echc.criterion_staging_id))

    if not all(i is None for i in check_id_errors):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR: missing FKs for el_criteria_has_criterion publication: {[error for error in check_id_errors if error]}")

    # Save echc for each value in publish object
    for val in echc.value_ids:
        echc_create = echc.dict()
        echc_create['value_id'] = val
        echc_save=ElCriteriaHasCriterionCreate(**echc_create)
        new_echc = await create_el_criteria_has_criterion(session=session, el_criteria_has_criterion=echc_save)

    # Call update method below - set criterion_staging echc criteria adjudication status to active
    stage_upd = CriterionStagingUpdate(id=echc.criterion_staging_id, el_criteria_has_criterion_id=new_echc.id, echc_adjudication_status=EchcAdjudicationStatus.ACTIVE)

    await criterion_staging_service.update(session=session, criterion=stage_upd, user_id=user_id)
    # update the study version status to "IN_PROCESS"
    study_version_to_upd = await study_version_crud.get_study_version_ec_id(current_session=session, eligibility_criteria_id = existing_staging.eligibility_criteria_id )
    await study_version_crud.update(db=session, db_obj=study_version_to_upd, obj_in={"status": StudyVersionStatus.IN_PROCESS})

    logger.info(f"User: {user_id} published el_criteria_has_criterion {new_echc.id} criterion_id: {new_echc.criterion_id} value_id: {new_echc.value_id} for study version {study_version_to_upd.id}")
    return new_echc
