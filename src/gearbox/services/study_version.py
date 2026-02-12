from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import HTTPException, Request
from gearboxdatamodel.models import StudyVersion, StudyVersion, Study
from gearboxdatamodel.schemas import StudyVersionCreate, StudyVersionSearchResults, StudyVersion as StudyVersionSchema, StudyVersionInfo, StudyVersionUpdate, StudyCreate, EligibilityCriteriaCreate
from gearboxdatamodel.util import status
from gearboxdatamodel.crud import study_version_crud, criterion_staging_crud, el_criteria_has_criterion_crud
from typing import List
from gearboxdatamodel.util.types import StudyVersionStatus, AdjudicationStatus, EchcAdjudicationStatus, EligibilityCriteriaStatus
from gearbox.services import criterion_staging as criterion_staging_service, study_algorithm_engine as study_algorithm_engine_service, study as study_service, eligibility_criteria as eligiblity_criteria_service, el_criteria_has_criterion as echc_service, value as value_service, match_form as match_form_service
from gearbox.util.qc import PublishStudyMessageDetail, PublishStudyMessage

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

    # find latest study version
    study_version.study_version_num = await get_latest_study_version(session, study_version.study_id) + 1

    # set others to inactive if incoming is active
    if study_version.status == StudyVersionStatus.ACTIVE:
        reset_active = await reset_active_status(session, study_version.study_id)
    new_study_version = await study_version_crud.create(db=session, obj_in=study_version)

    # await session.commit() 
    return new_study_version

async def update_study_version(session: Session, study_version: StudyVersionUpdate, request: Request=None, update_fe_files: bool=True) -> StudyVersionSchema:
    study_version_in = await study_version_crud.get(db=session, id=study_version.id)
    if study_version_in:
        upd_study_version = await study_version_crud.update(db=session, db_obj=study_version_in, obj_in=study_version)
    else:
        logger.error(f"Study version for id: {study_version.id} not found for update.") 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study version for id: {study_version.id} not found for update.") 
    await session.commit() 

    #update fe matching files and middleware cache after study version updated
    if update_fe_files:
        await study_service.refresh_study_fe_files(session=session, request=request)
    return upd_study_version


async def publish_study_version(session: Session, request: Request, study_version_id: int, ignore_warnings: bool = False):

    publish_errors = []
    publish_warnings = []

    logger.info(f"Publishing study version id: {study_version_id}")
    # get study_version
    study_version = await study_version_crud.get(db=session, id=study_version_id)
    if not study_version:
        msg=(f"Study version for id: {study_version_id} not found for publishing.") 
        publish_errors.append(PublishStudyMessage(message=msg))
        logger.error(f"{msg}")

    # Check for existing ACTIVE study_versions for the study
    # *** ERROR ***
    existing_active_svs = await study_version_crud.get_multi(session, 
        where=[f"{StudyVersion.__table__.name}.study_id = {study_version.study_id} and {StudyVersion.__table__.name}.status = '{StudyVersionStatus.ACTIVE.value}'"])
    if existing_active_svs:
        msg = (f"ACTIVE study versions already exist for id: {[x.id for x in existing_active_svs]}.") 
        logger.error(f"{msg}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{msg}")

    # Get all echc rows
    echcs = await el_criteria_has_criterion_crud.get_echc_by_ec_id(current_session=session, ec_id=study_version.eligibility_criteria_id)
    # Get all staging rows
    staging = await criterion_staging_crud.get_criterion_staging_by_ec_id(db=session, eligibility_criteria_id=study_version.eligibility_criteria_id)

    # check all rows in criterion_staging are 'ACTIVE' or 'INACTIVE' criterion_adjudication_status
    # *** ERROR ***
    invalid_status = list(set([x for x in AdjudicationStatus]) - set([AdjudicationStatus.ACTIVE, AdjudicationStatus.INACTIVE]))

    # get staging rows that have invalid status
    invalid_criterion_status = [ x for x in staging if x.criterion_adjudication_status in invalid_status]
    if invalid_criterion_status:
        msg = (f"The following criteria have not yet been fully adjudicated:")
        details = [PublishStudyMessageDetail(code=x.code, value=x.text) for x in invalid_criterion_status]
        publish_errors.append(PublishStudyMessage(message=msg, details=details))
        logger.error(f"{msg}:{[x.code for x in invalid_criterion_status]}.") 

    # check at least one active criterion for the study version
    # *** ERROR ***
    fully_adjudicated = [
        x for x in staging 
        if x.criterion_adjudication_status == AdjudicationStatus.ACTIVE and
        x.echc_adjudication_status == EchcAdjudicationStatus.ACTIVE 
        ]
    if len(fully_adjudicated) == 0:
        msg = (f"The study version must have at least one active criterion in order to be published.")
        publish_errors.append(PublishStudyMessage(message=msg))
        logger.error(f"{msg}")

    # check criterion_id exists for all rows in the criterion_staging table for the study_version
    # for ACTIVE status criteria 
    # *** ERROR ***
    staging_missing_criterion = [ x for x in fully_adjudicated if x.criterion_id == None ]
    if staging_missing_criterion:
        msg = (f"The following staged criteria have been adjudicated but are missing criterion ids:") 
        details = [PublishStudyMessageDetail(code=x.code, value=x.text) for x in staging_missing_criterion]
        publish_errors.append(PublishStudyMessage(message=msg, details=details))
        logger.error(f"{msg}: {[x.code for x in staging_missing_criterion]}")

    # check all criterion_ids in criterion_staging are for ACTIVE criteria (criterion.active = True) for criteria used
    # in the study (criterion_adjudication_status and echc_adjudication_status are both ACTIVE)
    # *** ERROR ***
    staging_inactive_criterion = await criterion_staging_service.get_criterion_staging_inactive_criterion(session=session, eligibility_criteria_id=study_version.eligibility_criteria_id)
    if staging_inactive_criterion:
        msg = (f"The following staged criteria are used in the study but are inactive:")
        details = [PublishStudyMessageDetail(code=x.code, value=x.text) for x in staging_inactive_criterion]
        publish_errors.append(PublishStudyMessage(message=msg, details=details))
        logger.error(f"{msg}: {[x.text for x in staging_inactive_criterion]}")

    # El criteria has criterion QC
    # check if study_algoritm_engine (study_version logic) exists for study_version
    # *** ERROR ***
    if not study_version.study_algorithm_engine:
        msg = (f"Study algorithm (study logic) does not yet exist for study version. See boolean logic builder tab.")
        publish_errors.append(PublishStudyMessage(message=msg))
        logger.error(f"{msg}: {study_version.id}") 

    # validate all echc ids in the study_algoritm_engine logic
    # *** ERROR ***
    invalid_echc_ids_in_logic = await study_algorithm_engine_service.validate_eligibility_criteria_ids(
        session=session, 
        algorithm_logic=study_version.study_algorithm_engine.algorithm_logic, 
        eligibility_criteria_id=study_version.eligibility_criteria_id)
    if invalid_echc_ids_in_logic:
        msg = (f"Study algorithm (study logic) contains the following invalid el_criteria_has_criterion.ids: \
               {invalid_echc_ids_in_logic}.")
        details = [PublishStudyMessageDetail(code=x) for x in invalid_echc_ids_in_logic]
        publish_errors.append(PublishStudyMessage(message=msg, details=details))
        logger.error(f"{msg}: {invalid_echc_ids_in_logic}") 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{msg}")

    # Check that all study criteria (questions) have display rules defined (i.e. exist in the match_form)
    # *** ERROR ***
    staged_criteria_criterion_t = await criterion_staging_service.get_staged_criteria_by_ec_id(session=session, eligibility_criteria_id=study_version.eligibility_criteria_id)
    criteria_not_in_match_form = []
    for sc in staged_criteria_criterion_t:
        if not sc.display_rules:
            criteria_not_in_match_form.append(sc)
    if criteria_not_in_match_form:
        msg = (f"The following criteria do not appear in the match form (missing display rules):")
        details = [PublishStudyMessageDetail(code=x.code) for x in criteria_not_in_match_form]
        publish_errors.append(PublishStudyMessage(message=msg, details=details))
        logger.error(f"{msg}:{[x.code for x in criteria_not_in_match_form]}") 
    
    # check for valid echc_ids in criterion_staging - each fully adjudicated row 
    # in the criterion_staging table should have at least one valid el_criteria_has_criterion id
    invalid_echc_ids=[]
    criterion_staging_missing_echc=[]
    staged_criteria = await criterion_staging_service.get_criterion_staging_by_ec_id(session=session, eligibility_criteria_id=study_version.eligibility_criteria_id)
    echcs = await echc_service.get_el_criteria_has_criterions_by_ecid(session=session, ecid=study_version.eligibility_criteria_id)
    valid_echc_ids = [x.id for x in echcs]

    for sc in staged_criteria:
        # Only do qc if criterion adjudication and echc adjudication status is active
        if sc.criterion_adjudication_status == AdjudicationStatus.ACTIVE and sc.echc_adjudication_status == EchcAdjudicationStatus.ACTIVE:
            if not sc.echc_ids:
                criterion_staging_missing_echc.append(sc)
            else:
                for staged_echc_id in sc.echc_ids:
                    if staged_echc_id not in valid_echc_ids:
                        invalid_echc_ids.append(staged_echc_id)

    if invalid_echc_ids:
        msg = (f"The following criterion_staging.echc_value_ids do not exist in the database for the study version: {invalid_echc_ids} ")
        details = [PublishStudyMessageDetail(code=x) for x in invalid_echc_ids]
        publish_errors.append(PublishStudyMessage(message=msg, details=details))
        logger.error(f"{msg} : {invalid_echc_ids}") 

    if criterion_staging_missing_echc:
        msg = (f"The following criterion_staging records are missing el_criteria_has_criterion ids:")
        details = [PublishStudyMessageDetail(code=x.code, value=x.text) for x in criterion_staging_missing_echc]
        publish_errors.append(PublishStudyMessage(message=msg, details=details))
        logger.error(f"{msg}: {criterion_staging_missing_echc}") 

    # QC echc_value_ids and criterion_value_ids    
    # *** ERROR ***
    valid_values = await value_service.get_values(session=session)
    valid_value_ids = [x.id for x in valid_values]
    invalid_echc_value_ids=[]
    invalid_criterion_value_ids=[]
    criterion_staging_missing_echc_value_ids=[]
    for sc in staged_criteria:

        if not sc.echc_value_ids:
            criterion_staging_missing_echc_value_ids.append(sc)
        else:
            for staged_value_id in sc.echc_value_ids:
                if staged_value_id not in valid_value_ids:
                    invalid_echc_value_ids.append(staged_value_id)

        if sc.criterion_value_ids:
            for staged_criterion_value_id in sc.criterion_value_ids:
                if staged_criterion_value_id not in valid_value_ids:
                    invalid_criterion_value_ids.append(staged_criterion_value_id)

    if invalid_echc_value_ids:
        msg = (f"The following criterion_staging.echc_value_ids do not exist in the database:")
        details = [PublishStudyMessageDetail(code=x) for x in invalid_echc_value_ids]
        publish_errors.append(PublishStudyMessage(message=msg, details=details))
        logger.error(f"{msg} : {invalid_echc_value_ids}") 

    if invalid_criterion_value_ids:
        msg = (f"The following criterion_staging.criterion_value_ids do not exist in the database:") 
        details = [PublishStudyMessageDetail(code=x) for x in invalid_criterion_value_ids]
        publish_errors.append(PublishStudyMessage(message=msg, details=details))
        logger.error(f"{msg} : {invalid_criterion_value_ids}") 

    if criterion_staging_missing_echc_value_ids:
        msg = (f"The following criterion_staging missing echc_value_ids:")
        details = [PublishStudyMessageDetail(code=x.code, value=x.text) for x in criterion_staging_missing_echc_value_ids]
        publish_errors.append(PublishStudyMessage(message=msg, details=details))
        logger.error(f"{msg} :  {[x.code for x in criterion_staging_missing_echc_value_ids]}") 

#------------------------------------------------- WARNINGS ------------------------------------
    if not ignore_warnings:
        # check all rows in criterion_staging are 'ACTIVE' or 'INACTIVE' echc_adjudication_status
        # *** WARNING ***
        invalid_echc_adjudication = await criterion_staging_service.get_criterion_staging_by_echc_criterion_adjudication_status(
            session=session, 
            eligibility_criteria_id=study_version.eligibility_criteria_id,
            echc_adjudication_status=[EchcAdjudicationStatus.NEW, EchcAdjudicationStatus.IN_PROCESS] 
        )
        if invalid_echc_adjudication:
            msg = (f"The following criterion_staging criteria are used in the study but el_criteria_has_criterion adjudication is not finalized:")
            details = [PublishStudyMessageDetail(code=x.code) for x in invalid_echc_adjudication]
            publish_warnings.append(PublishStudyMessage(message=msg, details=details))
            logger.warning(f"{msg}: {[x.code for x in invalid_echc_adjudication]}")

        # *** WARNING
        # Check for study version values (el_criteria_has_criterion rows) that are in the
        # staging table for the study version but do not occur in the study logic
        unused_echc_in_logic = await study_algorithm_engine_service.find_unused_eligibility_criteria(
            session=session, 
            algorithm_logic=study_version.study_algorithm_engine.algorithm_logic, 
            eligibility_criteria_id=study_version.eligibility_criteria_id)
        if unused_echc_in_logic:
            msg = (f"The following eligibility criteria were defined for the study but do not exist in the logic:")
            details = [PublishStudyMessageDetail(code=x.criterion.code, value=x.value.value_string) for x in unused_echc_in_logic]
            publish_warnings.append(PublishStudyMessage(message=msg, details=details))
            logger.warning(f"{msg}: {[(x.criterion.code, x.value.value_string) for x in unused_echc_in_logic]}")
        
        # Only return warnings if ignore_warnings param is false
        errors_warnings = []
        errors_warnings = {"publish_errors": [x.to_dict() for x in publish_errors], "publish_warnings": [x.to_dict() for x in publish_warnings]} 
        if publish_errors:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, errors_warnings)

        elif publish_warnings and not ignore_warnings:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, errors_warnings)
    # -- Warnings end

    # ---- STEPS TO PUBLISH ---
    # update study to active
    study = StudyCreate(active=True)
    noload_rel=[Study.study_versions]
    await study_service.update_study(session=session, study=study, study_id=study_version.study_id, noload_rel=noload_rel)

    # update study version to active
    study_version_upd=StudyVersionUpdate(id=study_version.id, status=StudyVersionStatus.ACTIVE)
    await update_study_version(session=session, study_version=study_version_upd, request=request)

    # update eligibility_criteria to active
    ec_upd = EligibilityCriteriaCreate(status=EligibilityCriteriaStatus.ACTIVE)
    await eligiblity_criteria_service.update_eligibility_criteria(session=session,eligibility_criteria=ec_upd, eligibility_criteria_id=study_version.eligibility_criteria_id)