from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional

class Value(BaseModel):
    id: int
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

class ValueCreate(BaseModel):
    pass

class ValueSearchResults(BaseModel):
    pass