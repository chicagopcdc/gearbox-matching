from urllib.request import HTTPDefaultErrorHandler
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Sequence, List, Optional

class StudyBase(BaseModel):
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

class Study(StudyBase):
    id: int

class StudyCreate(StudyBase):
    pass

class StudySearchResults(BaseModel):
    results: Sequence[Study]