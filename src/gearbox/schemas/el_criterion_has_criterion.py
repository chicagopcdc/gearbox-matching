from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional
from .value import Value
from .input_type import InputType
# from .criterion import CriterionBase

class ElCriterionHasCriterionBase(BaseModel):
    id: int
    criterion_id: int
    eligibility_criteria_id: int
    create_date: Optional[datetime]
    active: Optional[bool]
    value_id: int
    value: Value
    class Config:
        orm_mode = True

class ElCriterionHasCriterion(ElCriterionHasCriterionBase):
    pass
#    criterion: CriterionBase

class ElCriterionHasCriterionCreate(BaseModel):
    pass

class ElCriterionHasCriterionSearchResults(BaseModel):
    pass
