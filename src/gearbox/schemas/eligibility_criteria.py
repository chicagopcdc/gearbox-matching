from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List
from .el_criterion_has_criterion_schema import ElCriterionHasCriterionSchema

class EligibilityCriteria(BaseModel):
    id: int
    create_date: datetime
    active: bool
    study_version_id: int
    el_criteria_has_criterions: List[ElCriterionHasCriterionSchema]
    # notes: 


class EligibilityCriteriaCreate(BaseModel):
    pass

class EligibilityCriteriaSearchResults(BaseModel):
    pass
