from pydantic import BaseModel, Json
from typing import List, Union

from enum import Enum

class OperatorEnum(str, Enum):
    op_and = "AND"
    op_or = "OR"
    op_eq = "eq"
    op_gt = "gt"
    op_gte = "gte"
    op_lte = "lte"
    op_lt = "lt"

class ShowIfCriterion(BaseModel):
    id: int
    value: Union[int, float, str]
    valueId: int
    operator: OperatorEnum

class ShowIfLogic(BaseModel):
    operator: OperatorEnum
    criteria: Union[List[ShowIfCriterion], 'ShowIfLogic']

class MatchFormGroup(BaseModel):
    id: int
    name: str

class MatchFormOption(BaseModel):
    value: Union[float, int]
    label: str
    description: str | None = None

class MatchFormField(BaseModel):
    id: int
    groupId: int
    name: str
    min: Union[float,int] | None = None
    max: Union[float,int] | None = None
    step: Union[float,int] | None = None
    placeholder: str | None = None
    label: str
    type: str
    options: List[MatchFormOption] | None = None
    showIf: ShowIfLogic | None = None

class MatchFormBase(BaseModel):
    groups: List[MatchFormGroup]
    fields: List[MatchFormField]

class MatchForm(MatchFormBase):
    pass