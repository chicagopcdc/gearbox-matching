from urllib.request import HTTPDefaultErrorHandler
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Sequence, List, Optional

class StudyVersionBase(BaseModel):
    study_id: int
    create_date: Optional[datetime]
    study_version: int
    active: Optional[bool]

    class Config:
        orm_mode = True    

class StudyVersion(StudyVersionBase):
    id: int

class StudyVersionCreate(StudyVersionBase):
    pass

class StudyVersionSearchResults(BaseModel):
    results: Sequence[StudyVersion]