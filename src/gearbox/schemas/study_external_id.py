from pydantic import BaseModel, HttpUrl
from typing import Sequence, Optional

class StudyExternalIdBase(BaseModel):
    study_id: int
    ext_id: str
    source: str
    source_url: Optional[HttpUrl] = None
    active: Optional[bool]= None

    class Config:
        from_attributes = True 

class StudyExternalIdCreate(BaseModel):

    ext_id: str
    source: str
    source_url: Optional[HttpUrl] = None
    active: Optional[bool]= None

class StudyExternalId(StudyExternalIdBase):
    id: int

class StudyExternalIdSearchResults(BaseModel):
    results: Sequence[StudyExternalId]
    

