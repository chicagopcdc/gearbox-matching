from pydantic import BaseModel, Extra
from datetime import datetime
from typing import Optional, Sequence, List
from .unit import Unit

class ValueBase(BaseModel):
    description: Optional[str]
    is_numeric: bool
    value_string: str
    unit_id: Optional[int]
    operator: str
    create_date: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True    


class Value(ValueBase):
    id: int

class ValueCreate(ValueBase):
    unit_name: Optional[str]
    pass

class ValueSave(ValueBase):
    pass

class ValueUpdate(BaseModel):
    pass

class ValueSearchResults(BaseModel):
    results: Sequence[Value]    