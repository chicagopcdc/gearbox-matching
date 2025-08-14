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

class TriggeredByBase(BaseModel):
    display_rules_id: int
    criterion_id: int
    value_id: int
    active: Optional[bool]
    path: Optional[str]
    value: Value
    criterion: Criterion

    class Config:
        from_attributes = True 

class TriggeredBy(TriggeredByBase):
    id: int

class TriggeredByCreate(BaseModel):
    display_rules_id: int
    criterion_id: int
    value_id: int
    path: Optional[str]

class TriggeredBySearchResults(BaseModel):
    results: Sequence[TriggeredBy]
