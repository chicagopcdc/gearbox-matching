# from tkinter.tix import DisplayStyle
from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict
from .criterion_has_tag import CriterionTag
from .criterion_has_value import CriterionValue
from .input_type import InputType
from .el_criterion_has_criterion import ElCriterionHasCriterionBase

class CriterionBase(BaseModel):
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

class Criterion(CriterionBase):
    tags: Optional[List[CriterionTag]]
    values: Optional[List[CriterionValue]]
    el_criteria_has_criterions: List[ElCriterionHasCriterionBase]

class CriterionCreate(BaseModel):
    code: Optional[str]
    display_name: Optional[str]
    description: Optional[str]
    active: Optional[bool]
    ontology_code_id: Optional[int]
    input_type_id: Optional[int]
    tags: Optional[List[CriterionTag]]

    class Config:
        orm_mode = True

class CriterionSearchResults(BaseModel):
    pass


