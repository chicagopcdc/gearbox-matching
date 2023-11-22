from pydantic import BaseModel, HttpUrl
from typing import Sequence, Optional
from datetime import datetime

class StudyExternalIdBase(BaseModel):
    study_id: int
    ext_id: str
    source: str
    source_url: Optional[HttpUrl] 
    active: Optional[bool]

    class Config:
        orm_mode = True 

class StudyExternalIdCreate(BaseModel):

    ext_id: str
    source: str
    source_url: Optional[HttpUrl] 
    active: Optional[bool]

class StudyExternalId(StudyExternalIdBase):
    id: int

class StudyExternalIdSearchResults(BaseModel):
    results: Sequence[StudyExternalId]
    

