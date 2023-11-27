from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict

class SiteHasStudyBase(BaseModel):
    study_id: int
    site_id: int
    active: Optional[bool]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True

class SiteHasStudy(SiteHasStudyBase):
    pass

class SiteHasStudyCreate(SiteHasStudyBase):
    pass

class SiteHasStudySearchResults(SiteHasStudyBase):
    results: Sequence[SiteHasStudy]
