from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional
from .value import Value
from .input_type import InputType

class ElCriteriaHasCriterionBase(BaseModel):
    criterion_id: int
    eligibility_criteria_id: int
    create_date: Optional[datetime]
    active: Optional[bool]
    value_id: int
    class Config:
        orm_mode = True

class ElCriteriaHasCriterion(ElCriteriaHasCriterionBase):
    id: int

class ElCriteriaHasCriterionCreate(BaseModel):
    echcs: Sequence[ElCriteriaHasCriterionBase]

class ElCriteriaHasCriterionSearchResults(BaseModel):
    results: Sequence[ElCriteriaHasCriterion]
