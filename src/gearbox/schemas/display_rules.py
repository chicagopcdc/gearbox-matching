from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional
from .value import Value
from .criterion import Criterion

# I S S U E: this schema does not produce accurate
# dictionaries - it duplicates the tags and input_values
# in the criterion schema even though those relationships
# are explicitly taken out of the query (noload)...
# this schema is not necessary for the functionality
# of the match_form. This note is just in case it becomes
# necessary as part of a future use case. 

class TriggeredBy(BaseModel):
    id: int
    display_rules_id: int
    criterion_id: int
    value_id: int
    active: Optional[bool]
    path: Optional[str]
    criterion: Criterion
    value: Value

    class Config:
        orm_mode = True

class DisplayRules(BaseModel):
    id: int
    criterion_id: int
    priority: int
    version: Optional[int]
    active: Optional[bool]
    triggered_bys: Optional[List[TriggeredBy]]
    criterion: Optional[Criterion]

    class Config:
        orm_mode = True

class DisplayRulesCreate(BaseModel):
    pass

class DisplayRulesSearchResults(BaseModel):
    pass
