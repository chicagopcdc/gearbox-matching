from __future__ import annotations
from pydantic import BaseModel, Json
from typing import Optional, List, Union, Dict, Any

class PreAnnotated(BaseModel):
    span: Optional[List[Union[str, int]]] = None
    matched_models: Optional[List[str]] = None
    is_standard_gb_var: Optional[bool] = None

class Entity(BaseModel):
    id: Optional[int] = None
    label: Optional[str] = None
    start_offset: Optional[int] = None
    end_offset: Optional[int] = None
    meta: Optional[Union[Json[Any],Dict]] 

class RawCriteriaBase(BaseModel):
    text: str
    id: Optional[int] = None
    uuid: Optional[str] = None
    nct: Optional[str] = None
    pre_annotated: Optional[List[PreAnnotated]] = None
    entities: Optional[List[Entity]] = None
    Comments: Optional[Union[List[str],List[Dict]]] = None
    relations: Optional[Union[List[str],List[Dict]]] = None

    class Config:
        orm_mode = True    


class RawCriteria(RawCriteriaBase):
    id: int
    eligibility_criteria_id: int
    input_id: Optional[str] = None

class RawCriteriaIn(RawCriteriaBase):
    pass 

class RawCriteriaCreate(BaseModel):
    eligibility_criteria_id: int
    input_id: Optional[Union[str,int]] = None
    data:  Union[Json[Any],Dict]

class RawCriteriaUpdate(RawCriteriaBase):
    pass 