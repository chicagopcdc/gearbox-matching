from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Optional
from .site_has_study import StudySite
from .study_link import StudyLink

class Study(BaseModel):
    id: int
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]
    sites: Optional[List[StudySite]]
    links: Optional[List[StudyLink]]
    fake: int

    class Config:
        orm_mode = True

class StudyCreate(BaseModel):
    name: str
    code: str
    description: str
    active: bool

class StudySearchResults(BaseModel):
    results: Sequence[Study]

class StudyResponse(BaseModel):
    current_date: str
    current_time: str
    status: str
    body: List[Study]
