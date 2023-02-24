from pydantic import BaseModel, HttpUrl
from typing import Sequence, Optional

class StudyLinkBase(BaseModel):
    name: Optional[str]
    href: Optional[HttpUrl]
    study_id: Optional[int]
    active: Optional[bool]

    class Config:
        orm_mode = True

class StudyLink(StudyLinkBase):
    id: int

class StudyLinkCreate(StudyLinkBase):
    pass

class StudyLinkSearchResults(BaseModel):
    results: Sequence[StudyLink]
