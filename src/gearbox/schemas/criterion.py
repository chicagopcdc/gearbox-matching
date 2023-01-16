# from tkinter.tix import DisplayStyle
from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict
from .criterion_tag import CriterionTag
from .criterion_value import CriterionValue
from .input_type import InputType
from .el_criteria_has_criterion import ElCriteriaHasCriterionBase

class CriterionBase(BaseModel):
    code: Optional[str]
    display_name: Optional[str]
    description: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]
    ontology_code_id: Optional[int]
    input_type_id: Optional[int]
    # input_type: InputType move to Criterion if needed for ORM select

    class Config:
        orm_mode = True

class Criterion(CriterionBase):
    id: int
    tags: Optional[List[CriterionTag]]
    values: Optional[List[CriterionValue]]
    el_criteria_has_criterions: List[ElCriteriaHasCriterionBase]

class CriterionCreate(CriterionBase):
    pass

class CriterionCreateIn(CriterionBase):
    tags: Optional[List[int]]
    values: Optional[List[int]]
    display_rules_priority: int
    display_rules_version: Optional[int]
    triggered_by_criterion_id: Optional[int]
    triggered_by_value_id: Optional[int]
    triggered_by_path: Optional[str]


class CriterionSearchResults(BaseModel):
    results: Sequence[Criterion]    