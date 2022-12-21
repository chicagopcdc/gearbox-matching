from pydantic import BaseModel, Extra
from datetime import datetime
from typing import Optional

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
    code: Optional[str]
    description: Optional[str]
    type: Optional[str]
    value_string: Optional[str]
    unit: Optional[str]
    operator: Optional[str]
    active: Optional[bool]
    
    class Config:
        orm_mode = True

class ValueSearchResult(BaseModel):
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