from . import logger
from sqlalchemy.ext.asyncio import AsyncSession as Session
from gearbox.schemas import StudyVersionEligibilityCriteriaCreate, StudyVersionEligibilityCriteria as StudyVersionEligibilityCriteriaSchema
from gearbox.services import study_version as study_version_service, eligibility_criteria as eligibility_criteria_service, el_criteria_has_criterion as el_criteria_has_criterion_service, eligibility_criteria_info as eligibility_criteria_info_service

async def create_study_version_eligibility_criteria(session: Session, study_version_eligibility_criteria: StudyVersionEligibilityCriteriaCreate) -> StudyVersionEligibilityCriteriaSchema:
    new_study_version = await study_version_service.create_study_version(session, study_version_eligibility_criteria.study_version) 
    new_eligibility_criteria = await eligibility_criteria_service.create_eligibility_criteria(session, study_version_eligibility_criteria.eligibility_criteria) 
    new_el_criteria_has_criterion = await el_criteria_has_criterion_service.create_el_criteria_has_criterion(session, study_version_eligibility_criteria.el_criteria_has_criterion) 
    new_echcs = [x.__dict__ for x in new_el_criteria_has_criterion]

    # GET STUDY VERSION ID FROM NEW STUDY VERSION
    study_version_eligibility_criteria.eligibility_criteria_info.study_version_id = new_study_version.id
    new_eligibility_criteria_info = await eligibility_criteria_info_service.create_eligibility_criteria_info(session, study_version_eligibility_criteria.eligibility_criteria_info) 

    new_study_version_eligibility_criteria = {}
    new_study_version_eligibility_criteria["study_version"] = new_study_version.__dict__
    new_study_version_eligibility_criteria["eligibility_criteria"] = new_eligibility_criteria.__dict__
    new_study_version_eligibility_criteria["el_criteria_has_criterion"] = {"echcs": new_echcs}
    new_study_version_eligibility_criteria["eligibility_criteria_info"] = new_eligibility_criteria_info.__dict__
    ret_val = StudyVersionEligibilityCriteriaSchema.parse_obj(new_study_version_eligibility_criteria)

    await session.commit() 

    return ret_val