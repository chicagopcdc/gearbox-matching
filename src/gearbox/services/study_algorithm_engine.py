import json
from datetime import datetime
from fastapi.encoders import jsonable_encoder

from gearbox.models.study_algorithm_engine import StudyAlgorithmEngine
from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select, exc
from fastapi import HTTPException
from gearbox.models import ElCriteriaHasCriterion, EligibilityCriteria, StudyVersion, EligibilityCriteriaInfo
from gearbox.schemas import StudyAlgorithmEngine as StudyAlgorithmEngineSchema
from gearbox.schemas import StudyAlgorithmEngineCreate, StudyAlgorithmEngineSearchResults, StudyAlgorithmEngineCreateInput
from sqlalchemy.sql.functions import func
from gearbox.util import status, json_utils
from gearbox.crud import study_algorithm_engine_crud, eligibility_criteria_info_crud
from gearbox.util.types import EligibilityCriteriaInfoStatus

async def get_study_algorithm_engine(session: Session, id: int) -> StudyAlgorithmEngineSchema:
    aes = await study_algorithm_engine_crud.get(session, id)
    return aes

async def get_study_algorithm_engines(session: Session) -> StudyAlgorithmEngineSearchResults:
    aes = await study_algorithm_engine_crud.get_multi(session)
    return aes

async def create_study_algorithm_engine(session: Session, study_algorithm_engine: StudyAlgorithmEngineCreateInput) -> StudyAlgorithmEngineSchema:

    sae_input_conv = jsonable_encoder(study_algorithm_engine)
    sae_create = {key:value for key,value in sae_input_conv.items() if key in StudyAlgorithmEngineCreate.__fields__.keys() }

    new_ae = await study_algorithm_engine_crud.create(db=session, obj_in=sae_create)
    await session.commit()    
    return new_ae

async def get_invalid_logic_ids(session: Session, algorithm_logic: str, eligibility_criteria_id: int) -> list:
    """
    description:
        The purpose of this function is to QC the el_criteria_has_criterion ids
        in the ALGORITHM_ENGINE.algorithm_logic json. It checks each
        el_criteria_has_criterion.id in the algorithm_logic json to validate 
        that it exists in the list of el_criteria_has_criterion ids 
        related to the study_version for which the algorithm_engine is being
        stored.

    args:
        algorithm_logic json
        study_version_id
    
    returns: list of el_criteria_has_criterion_id from the algorithm_logic input, 
        that are not present in the el_criteria_has_criterion table for the study
    """
    try:
        result = await session.execute(select(ElCriteriaHasCriterion.id)
            .join(ElCriteriaHasCriterion.eligibility_criteria)
            .where(EligibilityCriteria.id == eligibility_criteria_id)
            .where(ElCriteriaHasCriterion.active == True)
        )
        db_el_criteria_has_criterion_ids = result.unique().scalars().all()
        input_el_criteria_has_criterion_ids = json_utils.json_extract_ints(algorithm_logic, 'criteria')

        # items that exist in input_el_criteria_has_criterion_ids but not in db_el_criteria_has_criterion_ids
        return list(set(input_el_criteria_has_criterion_ids).difference(db_el_criteria_has_criterion_ids))

    except exc.SQLAlchemyError as e:
        logger.error(f"SQL ERROR IN get_invalid_logic_ids method: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        


async def get_latest_algorithm_version(session: Session, study_version_id: int) -> int:
    try:
        result = await session.execute(select(func.max(StudyAlgorithmEngine.algorithm_version))
            .join(StudyAlgorithmEngine.eligibility_criteria_info)
            .where(EligibilityCriteriaInfo.study_version_id == study_version_id)
        )

        latest_algorithm_version = result.scalar_one()
    except exc.SQLAlchemyError as e:
        logger.error(f"SQL ERROR IN get_latest_algorithm_version method: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

    if latest_algorithm_version:
        return latest_algorithm_version
    else:
        return 0

async def get_existing_algorithm_logic_duplicate(session: Session, algorithm_logic: str, study_version_id: int) -> StudyAlgorithmEngine:
    """
    description:
        The purpose of this function is to find any existing
        exact duplicate algorithm_logic json for a particular study version
        in the algorithm_engine table. If a duplicate is found, the id
        of the duplicate row is returned which can then be used to assign
        to the appropriate study_version.
    """
    try:

        result = await session.execute(
            select(StudyAlgorithmEngine)
                .where(StudyAlgorithmEngine.id.in_(
                        select(EligibilityCriteriaInfo.study_algorithm_engine_id)
                                .where(EligibilityCriteriaInfo.study_version_id == study_version_id)
                        )
                )
        )
        

        # * SQLAlchemy note * scalars().all() returns a list of db model types 
        # just .all() returns a list of SQLAlchemy row type 
        existing_algorithms = result.scalars().all()

    except exc.SQLAlchemyError as e:
        logger.error(f"SQL ERROR IN get_existing_algorithm_logic_duplicate: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR: {type(e)}: {e}")        

    if existing_algorithms:
        for ex in existing_algorithms:
            a, b = json.dumps(ex.algorithm_logic), json.dumps(algorithm_logic)
            if a == b:
                return ex

    return None

async def reset_active_status(session: Session, study_version_id: int) -> bool:
    # set all rows related to the study_version to false
    eci_to_update = await eligibility_criteria_info_crud.get_multi(
        db=session,
        where=[f"eligibility_criteria_info.study_version_id = {study_version_id}"]
    )
    for sae in eci_to_update:
        # reset any currently 'ACTIVE' status to 'INACTIVE'
        if sae.status == EligibilityCriteriaInfoStatus.ACTIVE.value:
            await eligibility_criteria_info_crud.update(db=session, db_obj=sae, obj_in={"status":EligibilityCriteriaInfoStatus.INACTIVE.value})
    return True
    
async def create(session: Session, study_algorithm_engine: StudyAlgorithmEngineCreateInput) -> StudyAlgorithmEngine:

    # Check el_criteria_has_criterion ids in incoming algoritm engine exist in the db
    invalid_ids = await get_invalid_logic_ids(session, study_algorithm_engine.algorithm_logic, study_algorithm_engine.eligibility_criteria_id) 
    if invalid_ids:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study algorithm logic contains the following invalid ids: {invalid_ids}.")

    # Find existing exact duplicate algorithm logic for the study version
    dup_study_algorithm_engine = await get_existing_algorithm_logic_duplicate(session, study_algorithm_engine.algorithm_logic, study_algorithm_engine.study_version_id)

    # if no duplicate is found, determine version and insert new study algorithm engine
    if not dup_study_algorithm_engine:
        study_algorithm_engine.algorithm_version = await get_latest_algorithm_version(session, study_algorithm_engine.study_version_id) + 1

        # set current active to false before creating 
        reset_active = await reset_active_status(session, study_algorithm_engine.study_version_id)
        if reset_active:
            new_study_algorithm_engine = await create_study_algorithm_engine(session, study_algorithm_engine)
            return new_study_algorithm_engine
        else:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Issue encountered updating status of study_algorithm_engine rows.")
    else: 
        # if incoming is 'active', but we find a duplicate, set existing duplicate record to 'active', set start_date to current
        # if incoming is not active and there is an exact duplicate then do nothing

        # set set all current active to false 
        reset_active = await reset_active_status(session, study_algorithm_engine.study_version_id)
        dt = datetime.now()
        # set existing to active 
        dup_row = await study_algorithm_engine_crud.get(db=session, id=dup_study_algorithm_engine.id)
        await study_algorithm_engine_crud.update(db=session, db_obj=dup_row, obj_in={"active":True})

        return dup_study_algorithm_engine
