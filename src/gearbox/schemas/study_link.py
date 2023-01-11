from urllib.request import HTTPDefaultErrorHandler
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Sequence, List, Optional

class StudyLinkBase(BaseModel):
    name: Optional[str]
    href: Optional[HttpUrl]
    active: Optional[bool]

    class Config:
        orm_mode = True

class StudyLink(StudyLinkBase):
    id: int
    study_id: int


class StudyLinkCreate(StudyLinkBase):
    study_id: int
    pass

class StudyLinkSearchResults(BaseModel):
    results: Sequence[StudyLink]
