from pydantic import BaseModel
from typing import List, Union, Optional

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

class ShowIfCriterionUpdate(BaseModel):
    id: int
    value: Union[int, float, str]
    valueId: Optional[int] = None
    operator: OperatorEnum
    unit: Optional[str] = None
    is_numeric: Optional[bool] = None

class ShowIfLogicUpdate(BaseModel):
    operator: OperatorEnum
    criteria: Union[List[ShowIfCriterionUpdate], 'ShowIfLogicUpdate']

class MatchFormGroup(BaseModel):
    id: int
    name: str

class MatchFormOption(BaseModel):
    value: Union[float, int]
    label: str
    description: Optional[str] = None

class MatchFormFieldBase(BaseModel):
    id: int
    groupId: int
    name: str
    min: Optional[Union[float,int]] = None
    max: Optional[Union[float,int]] = None
    step: Optional[Union[float,int]]  = None
    placeholder: Optional[str] = None
    label: str
    type: str
    options: Optional[List[MatchFormOption]] = None

class MatchFormField(MatchFormFieldBase):
    showIf: Optional[ShowIfLogic] = None

class MatchFormFieldUpdate(MatchFormFieldBase):
    showIf: Optional[ShowIfLogicUpdate] = None

class MatchFormBase(BaseModel):
    groups: List[MatchFormGroup]
    fields: List[MatchFormField]

class MatchForm(MatchFormBase):
    fields: List[MatchFormField]

class MatchFormUpdate(MatchFormBase):
    fields: List[MatchFormFieldUpdate]