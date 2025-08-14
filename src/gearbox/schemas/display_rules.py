from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional
from .value import Value
from .criterion import Criterion
from .triggered_by import TriggeredBy

class DisplayRulesBase(BaseModel):
    id: int
    criterion_id: int
    priority: int
    version: Optional[int]
    active: Optional[bool]
    triggered_bys: Optional[List[TriggeredBy]]
    criterion: Criterion

    class Config:
        from_attributes = True 
    
class DisplayRules(DisplayRulesBase):
    pass

class DisplayRulesCreate(BaseModel):
    criterion_id: int
    priority: int
    version: Optional[int]

class DisplayRulesSearchResults(BaseModel):
    results: Sequence[DisplayRules]
