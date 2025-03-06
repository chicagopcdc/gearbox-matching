from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import HTTPException
from gearbox.models import StudyVersion, StudyVersion, Study
from gearbox.schemas import StudyVersionCreate, StudyVersionSearchResults, StudyVersion as StudyVersionSchema, StudyVersionInfo, StudyVersionUpdate, StudyCreate, EligibilityCriteriaCreate
from sqlalchemy.sql.functions import func
from gearbox.util import status
from gearbox.crud import study_version_crud 
from typing import List
from gearbox.util.types import StudyVersionStatus, AdjudicationStatus, EchcAdjudicationStatus, EligibilityCriteriaStatus
from gearbox.services import criterion_staging as criterion_staging_service, study_algorithm_engine as study_algorithm_engine_service, study as study_service, eligibility_criteria as eligiblity_criteria_service

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

    # check all rows in criterion_staging are 'ACTIVE' or 'INACTIVE' criterion_adjudication_status
    invalid_status = list(set([x for x in AdjudicationStatus]) - set([AdjudicationStatus.ACTIVE, AdjudicationStatus.INACTIVE]))
    invalid_criterion_adjudication = await criterion_staging_service.get_criterion_staging_by_criterion_adjudication_status(
        session=session, 
        eligibility_criteria_id=study_version.eligibility_criteria_id, 
        adjudication_status = invalid_status
    )
    if invalid_criterion_adjudication:
        qc_errors.append(f"The following staged criteria require final adjudication: {[x.id for x in invalid_criterion_adjudication ]}")

    # check criterion_id exists for all rows in the criterion_staging table for the study_version
    staging_missing_criterion = await criterion_staging_service.get_criterion_staging_missing_criterion_id(session=session, eligibility_criteria_id=study_version.eligibility_criteria_id)
    if staging_missing_criterion:
        qc_errors.append(f"The following criterion_staging ids are missing criterion ids: {[x.id for x in staging_missing_criterion]}")

    # check all criterion_ids in criterion_staging are for ACTIVE criteria
    staging_inactive_criterion = await criterion_staging_service.get_criterion_staging_inactive_criterion(session=session, eligibility_criteria_id=study_version.eligibility_criteria_id)
    if staging_inactive_criterion:
        qc_errors.append(f"The following criterion_staging ids are used in the study but are inactive: {[x.criterion_id for x in staging_missing_criterion]}")

    # check all rows in criterion_staging are 'ACTIVE' or 'INACTIVE' echc_adjudication_status
    invalid_echc_adjudication = await criterion_staging_service.get_criterion_staging_by_echc_criterion_adjudication_status(
        session=session, 
        eligibility_criteria_id=study_version.eligibility_criteria_id,
        echc_adjudication_status=[EchcAdjudicationStatus.NEW, EchcAdjudicationStatus.IN_PROCESS] 
    )
    if invalid_echc_adjudication:
        qc_errors.append(f"The following criterion_staging ids are used in the study but are inactive: {[x.id for x in invalid_echc_adjudication]}")

    # check if study_algoritm_engine (study_version logic) exists for study_version
    if not study_version.study_algorithm_engine:
        qc_errors.append(f"Study algorithm (study logic) does not exist for study version.")

    # validate all echc ids in the study_algoritm_engine logic
    invalid_echc_ids_in_logic = await study_algorithm_engine_service.validate_eligibility_criteria_ids(
        session=session, 
        algorithm_logic=study_version.study_algorithm_engine.algorithm_logic, 
        eligibility_criteria_id=study_version.eligibility_criteria_id)
    if invalid_echc_ids_in_logic:
        qc_errors.append(f"Study algorithm (study logic) contains the following invalid el_criteria_has_criterion.ids: {invalid_echc_ids_in_logic}.")

    # Check that all study criteria (questions) have display rules defined (i.e. exist in the match_form)
    staged_criteria = await criterion_staging_service.get_staged_criteria_by_ec_id(session=session, eligibility_criteria_id=study_version.eligibility_criteria_id)
    criteria_not_in_match_form = []
    for sc in staged_criteria:
        if not sc.display_rules:
            criteria_not_in_match_form.append(sc.id)
    if criteria_not_in_match_form:
        qc_errors.append(f"The following criteria do not appear in the match form: {criteria_not_in_match_form}")

    # log and raise exception for any qc errors 
    if qc_errors:
        logger.error(f"Errors found in study_version publish process: {qc_errors}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{qc_errors}")

    # ---- STEPS TO PUBLISH ---
    # update study to active
    study = StudyCreate(active=True)
    noload_rel=[Study.study_versions]
    await study_service.update_study(session=session, study=study, study_id=study_version.study_id, noload_rel=noload_rel)

    # update study version to active
    study_version_upd=StudyVersionUpdate(id=study_version.id, status=StudyVersionStatus.ACTIVE)
    await update_study_version(session=session, study_version=study_version_upd)

    # update eligibility_criteria to active
    ec_upd = EligibilityCriteriaCreate(status=EligibilityCriteriaStatus.ACTIVE)
    await eligiblity_criteria_service.update_eligibility_criteria(session=session,eligibility_criteria=ec_upd, eligibility_criteria_id=study_version.eligibility_criteria_id)
