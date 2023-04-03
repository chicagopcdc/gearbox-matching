from gearbox.schemas import StudyVersionCreate, ElCriteriaHasCriterionCreate, EligibilityCriteriaCreate, EligibilityCriteriaInfoCreate
from pydantic import BaseModel


class StudyVersionEligibilityCriteriaBase(BaseModel):
    study_version: StudyVersionCreate
    eligibility_criteria: EligibilityCriteriaCreate
    el_criteria_has_criterion: ElCriteriaHasCriterionCreate
    eligibility_criteria_info: EligibilityCriteriaInfoCreate

class StudyVersionEligibilityCriteriaCreate(StudyVersionEligibilityCriteriaBase):
    pass

class StudyVersionEligibilityCriteria(StudyVersionEligibilityCriteriaBase):
    pass