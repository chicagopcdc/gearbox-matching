from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional
from .criterion_schema import CriterionSchema
# from .criterion_has_tag import CriterionHasTag

class TriggeredBy(BaseModel):
    id: int
    display_rules_id: int
    criterion_id: int
    value_id: int
    active: Optional[bool]
    path: Optional[str]

    class Config:
        orm_mode = True

class DisplayRules(BaseModel):
    id: int
    criterion_id: int
    priority: int
    version: Optional[int]
    active: Optional[bool]
    triggered_bys: Optional[List[TriggeredBy]]
    criterion: Optional[CriterionSchema]

    class Config:
        orm_mode = True

class DisplayRulesCreate(BaseModel):
    pass

class DisplayRulesSearchResults(BaseModel):
    pass
