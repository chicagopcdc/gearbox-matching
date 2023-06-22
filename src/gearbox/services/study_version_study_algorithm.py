from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import exc, select
from gearbox.schemas import StudyVersionStudyAlgorithmCreate, StudyVersionStudyAlgorithm as StudyVersionStudyAlgorithmSchema
from gearbox.services import study_algorithm_engine as study_algorithm_engine_service
from gearbox.crud import eligibility_criteria_info_crud, study_version_crud
from fastapi import HTTPException
from gearbox.util import status
from gearbox.models import EligibilityCriteriaInfo
from gearbox.util.types import EligibilityCriteriaInfoStatus

async def create_study_version_study_algorithm(session: Session, study_version_study_algorithm: StudyVersionStudyAlgorithmCreate) -> StudyVersionStudyAlgorithmSchema:

    eligibility_criteria_info_id = study_version_study_algorithm.eligibility_criteria_info_id

    # get the eligibility_criteria_id from eligibility_criteria_info
    try:
        result = await session.execute(select(EligibilityCriteriaInfo)
            .where(EligibilityCriteriaInfo.id == eligibility_criteria_info_id))
        eligibility_criteria_info_db = result.unique().scalar_one()

        eligibility_criteria_id = eligibility_criteria_info_db.eligibility_criteria_id
        study_version_id = eligibility_criteria_info_db.study_version_id

    except exc.SQLAlchemyError as e:
        logger.error(f"SQL ERROR IN get_latest_study_version method: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")

    # add eligibility_criteria_id to study_version_study_algorithm

    study_version_study_algorithm.study_algorithm_engine.eligibility_criteria_id = eligibility_criteria_id
    new_study_algorithm_engine = await study_algorithm_engine_service.create(session=session, study_algorithm_engine=study_version_study_algorithm.study_algorithm_engine)

    # update eligibility_criteria_info with study_algorithm_engine.id and set to active
    ecii_upd = {
        "study_algorithm_engine_id": new_study_algorithm_engine.id,
        "status": EligibilityCriteriaInfoStatus.ACTIVE.value
    }
    eciid_in = await eligibility_criteria_info_crud.get(db=session, id=eligibility_criteria_info_id)
    if eciid_in:
        upd_value = await eligibility_criteria_info_crud.update(db=session, db_obj=eciid_in, obj_in=ecii_upd)
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Eligibility_criteria_info for id: {eligibility_criteria_info_id} not found for update.")

    new_study_version_study_algorithm = {}
    new_study_version_study_algorithm["eligibility_criteria_info_id"] = eligibility_criteria_info_id
    new_study_version_study_algorithm["study_algorithm_engine"] = new_study_algorithm_engine
    ret_val = StudyVersionStudyAlgorithmSchema.parse_obj(new_study_version_study_algorithm)
    return ret_val