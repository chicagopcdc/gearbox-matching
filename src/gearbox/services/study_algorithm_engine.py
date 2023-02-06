from cgitb import reset
import json
from datetime import datetime

from gearbox.models.study_algorithm_engine import StudyAlgorithmEngine
from . import logger
from sqlalchemy.orm import Session
from sqlalchemy import select, exc, update
from fastapi import HTTPException
from gearbox.models import ElCriteriaHasCriterion, EligibilityCriteria, StudyVersion
from gearbox.schemas import StudyAlgorithmEngine as StudyAlgorithmEngineSchema
from gearbox.schemas import StudyAlgorithmEngineCreate, StudyAlgorithmEngineSearchResults
from sqlalchemy.sql.functions import func
from gearbox.util import status, json_utils
from gearbox.crud import study_algorithm_engine_crud

async def get_study_algorithm_engine(session: Session, id: int) -> StudyAlgorithmEngineSchema:
    aes = await study_algorithm_engine_crud.get(session, id)
    return aes

async def get_study_algorithm_engines(session: Session) -> StudyAlgorithmEngineSearchResults:
    aes = await study_algorithm_engine_crud.get_multi(session)
    return aes
    pass

async def create_study_algorithm_engine(session: Session, study_algorithm_engine: StudyAlgorithmEngineCreate) -> StudyAlgorithmEngineSchema:

    new_ae = await study_algorithm_engine_crud.create(db=session, obj_in=study_algorithm_engine)
    await session.commit()    
    return new_ae

async def check_study_version_id_exists(session: Session, study_version_id_in: int):
    try:
        result = await session.execute(select(StudyVersion.id).
            where(StudyVersion.id == study_version_id_in))
        study_version_id = result.scalar_one()
    except exc.SQLAlchemyError as e:
        logger.error(f"SQL ERROR IN check_study_version_id method: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")        

    return True if study_version_id else False

async def get_invalid_logic_ids(session: Session, algorithm_logic: str, study_version_id: int) -> list:
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
            .where(EligibilityCriteria.study_version_id == study_version_id)
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
            .where(StudyAlgorithmEngine.study_version_id == study_version_id)
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

        result = await session.execute(select(StudyAlgorithmEngine)
            .where(StudyAlgorithmEngine.study_version_id == study_version_id)
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
    sae_to_update = await study_algorithm_engine_crud.get_multi(
        db=session, 
        active=False, 
        where=[f"study_algorithm_engine.study_version_id = {study_version_id}"]
    )
    for sae in sae_to_update:
        # set all to false
        await study_algorithm_engine_crud.update(db=session, db_obj=sae, obj_in={"active":False})
    return True
    
async def create(session: Session, study_algorithm_engine: StudyAlgorithmEngineCreate) -> StudyAlgorithmEngine:
    # Check if study version on incoming algorithm engine exists in the db
    if not await check_study_version_id_exists(session, study_algorithm_engine.study_version_id):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study_version {study_algorithm_engine.study_version_id} does not exist.")

    # Check el_criteria_has_criterion ids in incoming algoritm engine exist in the db
    invalid_ids = await get_invalid_logic_ids(session, study_algorithm_engine.algorithm_logic, study_algorithm_engine.study_version_id) 
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