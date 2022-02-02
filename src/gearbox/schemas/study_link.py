from urllib.request import HTTPDefaultErrorHandler
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Sequence, List, Optional

class StudyLink(BaseModel):
    id: int
    study_id: int
    name: Optional[str]
    href: Optional[HttpUrl]
    active: Optional[bool]

    class Config:
        orm_mode = True


class StudyLinkCreate(BaseModel):
    pass

class StudyLinkSearchResults(BaseModel):
    pass
