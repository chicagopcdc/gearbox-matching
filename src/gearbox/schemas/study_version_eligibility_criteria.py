from gearbox.schemas import StudyVersionCreate, ElCriteriaHasCriterionCreate, EligibilityCriteriaCreate, EligibilityCriteriaInfoCreate
from gearbox.schemas import EligibilityCriteria, EligibilityCriteriaInfo, ElCriteriaHasCriterions
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
    eligibility_criteria: Optional[EligibilityCriteria]
    el_criteria_has_criterion: ElCriteriaHasCriterions
    eligibility_criteria_info: Optional[EligibilityCriteriaInfo]