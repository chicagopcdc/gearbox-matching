from sqlalchemy.ext.asyncio import AsyncSession as Session
import json
from . import logger
from fastapi import HTTPException
from gearbox.models import RawCriteria
from gearbox.schemas import RawCriteriaCreate, RawCriteria as RawCriteriaSchema, StudyVersionCreate, RawCriteriaIn, CriterionStagingCreate, CriterionStagingUpdate
from gearbox.util import status 
from gearbox.util.types import StudyVersionStatus, AdjudicationStatus, EchcAdjudicationStatus
from gearbox.crud import raw_criteria_crud, criterion_crud, study_version_crud
from gearbox.services import study as study_service, study_version as study_version_service, eligibility_criteria as eligibility_criteria_service, criterion_staging as criterion_staging_service
from typing import List

async def get_raw_criteria(session: Session, id: int) -> RawCriteriaSchema:
    raw_crit = await raw_criteria_crud.get(session, id)
    return raw_crit

async def get_raw_criteria_by_eligibility_criteria_id(session: Session, eligibility_criteria_id: int):
    raw_crit = await raw_criteria_crud.get_by_eligibility_criteria_id(session, eligibility_criteria_id=eligibility_criteria_id)
    return raw_crit

async def get_raw_criterias(session: Session) -> List[RawCriteria]:
    raw_crit = await raw_criteria_crud.get_multi(session)
    return raw_crit

async def create_staging_criterion(session: Session, input_id: int, eligibility_criteria_id: int,
        code: str, start_span: int, end_span:int, text: str):

        criterion_id = await criterion_crud.get_criterion_id_by_code(db=session, code=code)

        csc = CriterionStagingCreate(
            input_id = input_id,
            eligibility_criteria_id = eligibility_criteria_id,
            code = code,
            criterion_adjudication_status = AdjudicationStatus.NEW.value if criterion_id == None else AdjudicationStatus.EXISTING.value,
            echc_adjudication_status = EchcAdjudicationStatus.NEW.value,
            start_char = start_span,
            end_char = end_span,
            text = text,
            criterion_id = criterion_id
        )

        res = await criterion_staging_service.create(session, csc)


async def stage_criteria(session: Session, raw_criteria: RawCriteria):

    raw_text = raw_criteria.data.get('text')
    input_id = raw_criteria.data.get('id')
    for label in raw_criteria.data.get('label'):

        ## get criterion_id from code
        code = label[2]
        criterion_id = await criterion_crud.get_criterion_id_by_code(db=session, code=code)

        start_span = label[0]
        end_span = label[1]

        await create_staging_criterion(session=session,
            input_id=input_id,
            eligibility_criteria_id=raw_criteria.eligibility_criteria_id,
            code=code,
            start_span=start_span,
            end_span=end_span,
            text = raw_text[start_span:end_span]
        )

def get_incoming_raw_criteria(raw_criteria: RawCriteriaIn)-> dict:
    extracted_crit = {}
    raw_text = raw_criteria.data.get('text')
    for labelinfo in raw_criteria.data.get('label'):
        code=labelinfo[2]
        start_span=labelinfo[0]
        end_span=labelinfo[1]
        text = raw_text[start_span:end_span]
        extracted_crit.update({(code,text):(start_span,end_span)})
    return extracted_crit

async def create_raw_criteria(session: Session, raw_criteria: RawCriteriaIn, user_id: int):

    """
    This function will create a new raw_criteria for adjudication along with associated
    relationships including: study_version, and eligibility_criteria,
    and criteria_staging. The criteria_staging table is used to stage the criteria
    for adjudication. 

    If the same study_version was re-uploaded from doccano, this function will save
    any adjudication that may have been performed on existing criteria and upload any 
    criteria that have not yet been staged. 
    """
    # Get the study_id for the study based on the id in the raw criteria json
    ext_id = raw_criteria.data.get("nct")
    study_id = await study_service.get_study_id_by_ext_id(session, ext_id)
    if not study_id:
         logger.error(f"Study for id: {ext_id} not found for update.") 
         raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Study for id: {ext_id} not found for update.") 
    
    # Get existing study_version if existsA
    latest_study_version = await study_version_crud.get_latest_study_version(current_session=session, study_id=study_id)

    if not latest_study_version or latest_study_version.status in (StudyVersionStatus.ACTIVE, StudyVersionStatus.INACTIVE):
        """
        If the study version does not exist or is currently active or inactive 
        create a new study version and associated relationships.
        """
    
        # Create a new eligibility criteria
        eligibility_criteria = await eligibility_criteria_service.create_eligibility_criteria(session)
        
        # Create a new study_version
        comments = ''.join(raw_criteria.data.get("Comments"))
        new_study_version = StudyVersionCreate(study_id=study_id, status=StudyVersionStatus.NEW, comments=comments, eligibility_criteria_id=eligibility_criteria.id)
        study_version = await study_version_service.create_study_version(session,new_study_version)

        # Save the new raw criteria to the db
        new_raw_criteria = RawCriteriaCreate(data=raw_criteria.data, eligibility_criteria_id=eligibility_criteria.id)
        raw_criteria = await raw_criteria_crud.create(db=session, obj_in=new_raw_criteria)

        # Create criterion_staging rows from the raw criteria json
        await stage_criteria(session, raw_criteria)
        logger.info(f"Raw criteria for study {ext_id} successfully staged.")

    else: 
        """
        This logic is for situations when the user re-uploads from doccano and the process
        needs to update the raw criteria and account for any changes to criteria in the 
        criteiron_staging table
        """
        criterion_staging = await criterion_staging_service.get_criterion_staging_by_ec_id(session=session , eligibility_criteria_id=latest_study_version.eligibility_criteria_id )
        incoming_raw_criteria = get_incoming_raw_criteria(raw_criteria)

        existing_staging = [(crit.code, crit.text) for crit in criterion_staging]        

        # Find any criteria in the incoming raw_criteria that do not exist
        # in the criterion_staging table. The comparison is based on
        # a tuple including (code, text)
        new_to_add = set(incoming_raw_criteria.keys()) - set(existing_staging)
        new_to_add_dict = {k:v for k,v in incoming_raw_criteria.items() if k in new_to_add}

        # get list of new_to_add raw_criteria objs and pass to stage func
        incoming_text = raw_criteria.data.get('text')
        for incoming in raw_criteria.data.get('label'):

            if new_to_add_dict.get((incoming[2],incoming_text[incoming[0]:incoming[1]])):
                await create_staging_criterion(session=session,
                    input_id=raw_criteria.data.get('id'),
                    eligibility_criteria_id=latest_study_version.eligibility_criteria_id,
                    code=incoming[2],
                    start_span=incoming[0],
                    end_span=incoming[1],
                    text = incoming_text[incoming[0]:incoming[1]]
                )
                    
        # set of criteria that do not exist in incoming - set to INACTIVE
        old_to_set_inactive = set(existing_staging) - set(incoming_raw_criteria.keys())
        # set of criteria that did not change (text) - update start/end char only
        # in case the raw text has changed
        existing_no_change = set(existing_staging).union(set(incoming_raw_criteria.keys()))
        for crit in criterion_staging:
            # set any criteria to INACTIVE that do not exist in incoming
            if (crit.code, crit.text) in old_to_set_inactive:
                crit.criterion_adjudication_status = AdjudicationStatus.INACTIVE
                await criterion_staging_service.update(session=session, criterion=crit, user_id=user_id)
            # only update start_char and end_char if no change in text
            elif (crit.code, crit.text) in existing_no_change:
                # get start_char and end-char from incoming_raw_criteria
                for inc in incoming_raw_criteria.keys():
                    if (crit.code, crit.text) == inc:
                        crit.start_char, crit.end_char = incoming_raw_criteria.get((inc))
                        await criterion_staging_service.update(session=session, criterion=crit, user_id=user_id)

        row = {
            'eligibility_criteria_id':latest_study_version.eligibility_criteria_id,
            'data':raw_criteria.data
        }

        await raw_criteria_crud.upsert(
            db=session,
            model=RawCriteria,
            row=row,
            constraint_cols=[RawCriteria.eligibility_criteria_id]
        )

async def update_raw_criteria(session: Session, raw_criteria: RawCriteriaCreate, raw_criteria_id: int):
    raw_criteria_in = await raw_criteria_crud.get(db=session, id=raw_criteria_id)
    if raw_criteria_in:
        await raw_criteria_crud.update(db=session, db_obj=raw_criteria_in, obj_in=raw_criteria)
    else:
        logger.error(f"Raw criteria id: {raw_criteria_id} not found for update.") 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Raw criteria id: {raw_criteria_id} not found for update.") 