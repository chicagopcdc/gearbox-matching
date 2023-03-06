from xml.dom.minidom import Identified
from pydantic import BaseModel, Extra
from datetime import datetime
from typing import Optional, Sequence, List, Union

class MatchFormGroup(BaseModel):
    id: int
    name: str

class MatchFormOption(BaseModel):
    value: Union[float, int]
    label: str
    description: Optional[str]

class MatchFormShowIfCriteria(BaseModel):
    id: Optional[int]
    value: Optional[Union[float,int]]
    operator: str

class MatchFormShowIf(BaseModel):
    operator: str
    criteria: List[MatchFormShowIfCriteria]

class MatchFormField(BaseModel):
    id: int
    groupId: int
    name: str
    min: Optional[Union[float,int]]
    max: Optional[Union[float,int]]
    step: Optional[Union[float,int]]
    placeholder: Optional[str]
    label: str
    type: str
    options: Optional[List[MatchFormOption]]
    showIf: Optional[MatchFormShowIf]


class MatchFormBase(BaseModel):
    groups: List[MatchFormGroup]
    fields: List[MatchFormField]

class MatchForm(MatchFormBase):
    pass
