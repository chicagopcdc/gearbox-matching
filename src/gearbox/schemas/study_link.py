from pydantic import BaseModel, HttpUrl
from typing import Sequence, Optional
from datetime import datetime

class StudyLinkBase(BaseModel):
    study_id: Optional[int] = None
    name: Optional[str] = None
    href: Optional[HttpUrl] = None
    active: Optional[bool] = None
    create_date: Optional[datetime] = None

    class Config:
        orm_mode = True

class StudyLink(StudyLinkBase):
    id: int

class StudyLinkCreate(StudyLinkBase):
    pass

class StudyLinkSearchResults(BaseModel):
    results: Sequence[StudyLink]
