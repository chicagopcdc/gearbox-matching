from sqlalchemy.ext.asyncio import AsyncSession as Session
from . import logger
from fastapi import HTTPException
from gearbox.models import RawCriteria
from gearbox.schemas import RawCriteriaCreate, RawCriteria as RawCriteriaSchema, StudyVersionCreate, RawCriteriaIn, CriterionStagingCreate
from gearbox.util import status 
from gearbox.util.types import StudyVersionStatus, AdjudicationStatus, EchcAdjudicationStatus
from gearbox.crud import raw_criteria_crud, criterion_crud
from gearbox.services import study as study_service, study_version as study_version_service, eligibility_criteria as eligibility_criteria_service, criterion_staging as criterion_staging_service
from typing import List

async def get_raw_criteria(session: Session, id: int) -> RawCriteriaSchema:
    raw_crit = await raw_criteria_crud.get(session, id)
    return raw_crit

async def get_raw_criteria_by_eligibility_criteria_id(session: Session, eligibility_criteria_id: int):
    raw_crit = await raw_criteria_crud.get_by_eligibility_criteria_id(session, eligibility_criteria_id=eligibility_criteria_id)
    raw_crit_text = raw_crit.get('text')
    return raw_crit_text

async def get_raw_criterias(session: Session) -> List[RawCriteria]:
    raw_crit = await raw_criteria_crud.get_multi(session)
    return raw_crit

async def stage_criteria(session: Session, raw_criteria: RawCriteria):

    raw_text = raw_criteria.data.get('text')
    input_id = raw_criteria.data.get('id')
    for label in raw_criteria.data.get('label'):

        ## get criterion_id from code
        code = label[2]
        criterion_id = await criterion_crud.get_criterion_id_by_code(db=session, code=code)

        start_span = label[0]
        end_span = label[1]

        csc = CriterionStagingCreate(
            input_id = input_id,
            eligibility_criteria_id = raw_criteria.eligibility_criteria_id,
            code = code,
            criterion_adjudication_status = AdjudicationStatus.NEW.value if criterion_id == None else AdjudicationStatus.EXISTING.value,
            echc_adjudication_status = EchcAdjudicationStatus.NEW.value,
            start_char = start_span,
            end_char = end_span,
            text = raw_text[start_span:end_span],
            criterion_id = criterion_id
        )

        res = await criterion_staging_service.create(session, csc)


async def create_raw_criteria(session: Session, raw_criteria: RawCriteriaIn):

    """
    This function will create a new raw_criteria for adjudication along with associated
    relationships including: study_version, and eligibility_criteria,
    and criteria_staging. The criteria_staging table is used to stage the criteria
    for adjudication. 
    """
    # Get the study_id for the study based on the id in the raw criteria json
    ext_id = raw_criteria.data.get("nct")
    study_id = await study_service.get_study_id_by_ext_id(session, ext_id)
    if not study_id:
         logger.error(f"Study for id: {ext_id} not found for update.") 
         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study for id: {ext_id} not found for update.") 
    
    # Create a new study_version
    comments = ''.join(raw_criteria.data.get("Comments"))
    new_study_version = StudyVersionCreate(study_id=study_id, status=StudyVersionStatus.NEW, comments=comments)
    study_version = await study_version_service.create_study_version(session,new_study_version)

    # Create a new eligibility criteria
    eligibility_criteria = await eligibility_criteria_service.create_eligibility_criteria(session)

    # Create the new raw criteria
    new_raw_criteria = RawCriteriaCreate(data=raw_criteria.data, eligibility_criteria_id=eligibility_criteria.id)
    raw_criteria = await raw_criteria_crud.create(db=session, obj_in=new_raw_criteria)

    await stage_criteria(session, raw_criteria)
    logger.info(f"Raw criteria for study {ext_id} successfully staged.")

async def update_raw_criteria(session: Session, raw_criteria: RawCriteriaCreate, raw_criteria_id: int):
    raw_criteria_in = await raw_criteria_crud.get(db=session, id=raw_criteria_id)
    if raw_criteria_in:
        upd_raw_criteria = await raw_criteria_crud.update(db=session, db_obj=raw_criteria_in, obj_in=raw_criteria)
    else:
        logger.error(f"Raw criteria id: {raw_criteria_id} not found for update.") 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Raw criteria id: {raw_criteria_id} not found for update.") 