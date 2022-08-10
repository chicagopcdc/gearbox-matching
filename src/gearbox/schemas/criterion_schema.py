# from tkinter.tix import DisplayStyle
from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict
from .criterion_has_tag import CriterionTag
from .criterion_has_value import CriterionValue
from .input_type import InputType
from .el_criterion_has_criterion_schema import ElCriterionHasCriterionSchema

class CriterionSchema(BaseModel):
    id: int
    code: Optional[str]
    display_name: Optional[str]
    description: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]
    ontology_code_id: Optional[int]
    input_type_id: Optional[int]
    tags: Optional[List[CriterionTag]]
    el_criteria_has_criterions: List[ElCriterionHasCriterionSchema]
    input_type: InputType
    values: Optional[List[CriterionValue]]

    class Config:
        orm_mode = True

class CriterionCreateSchema(BaseModel):
    pass

class CriterionSearchResultsSchema(BaseModel):
    pass


