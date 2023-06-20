from gearbox.schemas import StudyVersionCreate, ElCriteriaHasCriterionCreate, EligibilityCriteriaCreate, EligibilityCriteriaInfoCreate
from pydantic import BaseModel
from typing import Optional

class StudyVersionEligibilityCriteriaBase(BaseModel):
    study_version: StudyVersionCreate
    eligibility_criteria: Optional[EligibilityCriteriaCreate]
    el_criteria_has_criterion: ElCriteriaHasCriterionCreate
    eligibility_criteria_info: Optional[EligibilityCriteriaInfoCreate]

class StudyVersionEligibilityCriteriaCreate(StudyVersionEligibilityCriteriaBase):
    pass

class StudyVersionEligibilityCriteria(StudyVersionEligibilityCriteriaBase):
    pass