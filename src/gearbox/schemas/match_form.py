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

class MatchFormField(BaseModel):
    id: int
    groupId: int
    name: str
    min: Optional[Union[float,int]] = None
    max: Optional[Union[float,int]] = None
    step: Optional[Union[float,int]] = None
    placeholder: Optional[str] = None
    label: str
    type: str
    options: Optional[List[MatchFormOption]] = None
    showIf: Optional[dict]

class MatchFormBase(BaseModel):
    groups: List[MatchFormGroup]
    fields: List[MatchFormField]

class MatchForm(MatchFormBase):
    pass
