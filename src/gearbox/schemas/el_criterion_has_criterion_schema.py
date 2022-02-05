from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional
from .value import Value
from .input_type import InputType
# from .criterion_schema import CriterionSchema

class CriterionSchema(BaseModel):
    id: int
    code: Optional[str]
    display_name: Optional[str]
    description: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]
    ontology_code_id: Optional[int]
    input_type_id: Optional[int]
    input_type: InputType
    class Config:
        orm_mode = True

class ElCriterionHasCriterionSchema(BaseModel):
    id: int
    criterion_id: int
    eligibility_criteria_id: int
    create_date: Optional[datetime]
    active: Optional[bool]
    value_id: int
    criterion: CriterionSchema
    value: Value
    class Config:
        orm_mode = True

class ElCriterionHasCriterionCreate(BaseModel):
    pass

class ElCriterionHasCriterionSearchResults(BaseModel):
    pass
