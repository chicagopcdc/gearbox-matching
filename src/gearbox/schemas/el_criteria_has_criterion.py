from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional
from .value import Value
from .input_type import InputType

class ElCriteriaHasCriterionBase(BaseModel):
    criterion_id: int
    eligibility_criteria_id: Optional[int] = None
    create_date: Optional[datetime] = None
    active: Optional[bool] = None
    class Config:
        orm_mode = True

class ElCriteriaHasCriterion(ElCriteriaHasCriterionBase):
    id: int

class ElCriteriaHasCriterions(BaseModel):
    echcs: Sequence[ElCriteriaHasCriterion]

class ElCriteriaHasCriterionCreate(ElCriteriaHasCriterionBase):
    value_id: int

class ElCriteriaHasCriterionPublish(ElCriteriaHasCriterionBase):
    criterion_staging_id: int
    value_ids: List[int]

class ElCriteriaHasCriterions(BaseModel):
    echcs: Sequence[ElCriteriaHasCriterion]

class ElCriteriaHasCriterionSearchResults(BaseModel):
    results: Sequence[ElCriteriaHasCriterion]