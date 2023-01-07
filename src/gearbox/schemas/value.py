from pydantic import BaseModel, Extra
from datetime import datetime
from typing import Optional, Sequence

class ValueBase(BaseModel):
    code: Optional[str]
    description: Optional[str]
    type: Optional[str]
    value_string: Optional[str]
    unit: Optional[str]
    operator: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True    


class Value(ValueBase):
    id: int

class ValueCreate(ValueBase):
    pass

class ValueUpdate(BaseModel):
    pass

class ValueSearchResults(BaseModel):
    results: Sequence[Value]    