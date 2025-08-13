import sre_compile
from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional

class PreAnnotatedCriterionBase(BaseModel):
    id: int
    raw_criteria_id: int
    text: Optional[str]
    label: Optional[str]
    is_standard_gb_var: Optional[bool]

    class Config:
        from_attributes = True 

class PreAnnotatedCriterion(PreAnnotatedCriterionBase):
    pass

class PreAnnotatedCriterionCreate(BaseModel):
    raw_criteria_id: int
    text: Optional[str]
    label: Optional[str]
    is_standard_gb_var: Optional[bool]

class PreAnnotatedCriterionSearchResults(BaseModel):
    results: Sequence[PreAnnotatedCriterion]
