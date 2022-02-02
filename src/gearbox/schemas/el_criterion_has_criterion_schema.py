from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional
from .value import Value

class ElCriterionHasCriterionSchema(BaseModel):
    id: int
    criterion_id: int
    eligibility_criteria_id: int
    create_date: Optional[datetime]
    active: Optional[bool]
    value_id: int

    class Config:
        orm_mode: True

class ElCriterionHasCriterionCreate(BaseModel):
    pass

class ElCriterionHasCriterionSearchResults(BaseModel):
    pass
