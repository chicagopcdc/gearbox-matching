from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional
from .value import Value
from .input_type import InputType
# from .criterion import CriterionBase

class ElCriteriaHasCriterionBase(BaseModel):
    id: int
    criterion_id: int
    eligibility_criteria_id: int
    create_date: Optional[datetime]
    active: Optional[bool]
    value_id: int
    value: Value
    class Config:
        orm_mode = True

class ElCriteriaHasCriterion(ElCriteriaHasCriterionBase):
    id: int
#    criterion: CriterionBase

class ElCriteriaHasCriterionCreate(ElCriteriaHasCriterionBase):
    pass

class ElCriteriaHasCriterionSearchResults(BaseModel):
    results: Sequence[ElCriteriaHasCriterion]
