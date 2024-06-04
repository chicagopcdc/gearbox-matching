from pydantic import BaseModel, ValidationError, validator
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
    status: Optional[str]
    ontology_code_id: Optional[int]
    input_type_id: int

    class Config:
        orm_mode = True

class Criterion(CriterionBase):
    id: int
    tags: Optional[List[CriterionTag]]
    values: Optional[List[CriterionValue]]
#    el_criteria_has_criterions: List[ElCriteriaHasCriterionBase]

class CriterionCreate(CriterionBase):
    code: str
    display_name: str

class CriterionCreateIn(CriterionBase):
    code: str
    tags: List[int]
    values: Optional[List[int]]
    display_rules_priority: int
    display_rules_version: Optional[int]
    triggered_by_criterion_id: Optional[int]
    triggered_by_value_id: Optional[int]
    triggered_by_path: Optional[str]


class CriterionSearchResults(BaseModel):
    results: Sequence[Criterion]    