from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from gearbox.schemas import Site

class SiteHasStudyBase(BaseModel):
    study_id: int
    site_id: int
    active: Optional[bool] = None
    create_date: Optional[datetime] = None
    site: Optional[Site] = None

    class Config:
        from_attributes = True 

class SiteHasStudySite(BaseModel):
    site: Optional[Site] = None

    class Config:
        from_attributes = True 

class SiteHasStudy(SiteHasStudyBase):
    pass

class SiteHasStudyCreate(SiteHasStudyBase):
    pass

class SiteHasStudySearchResults(SiteHasStudyBase):
    results: Sequence[SiteHasStudy]
