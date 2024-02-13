from pydantic import BaseModel, Extra
from datetime import datetime
from typing import Optional, Sequence, List
from .unit import Unit

class ValueBase(BaseModel):
    description: Optional[str]
    type: Optional[str]
    value_string: Optional[str]
    unit_id: Optional[Unit]
    operator: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True    


class Value(ValueBase):
    id: int

class ValueCreate(ValueBase):
    unit_name: Optional[str]
    pass

class ValueUpdate(BaseModel):
    pass

class ValueSearchResults(BaseModel):
    results: Sequence[Value]    