from urllib.request import HTTPDefaultErrorHandler
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Sequence, List, Optional

class StudyLinkBase(BaseModel):
    name: Optional[str]
    href: Optional[HttpUrl]
    study_id: int
    active: Optional[bool]

    class Config:
        orm_mode = True

class StudyLink(StudyLinkBase):
    id: int


class StudyLinkCreate(StudyLinkBase):
    pass

class StudyLinkSearchResults(BaseModel):
    results: Sequence[StudyLink]
