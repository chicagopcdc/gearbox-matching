#from urllib.request import HTTPDefaultErrorHandler
from pydantic import BaseModel #, HttpUrl
from datetime import datetime
from typing import Sequence, List, Optional, Any
from gearbox.schemas import SiteCreate #, StudyLinkCreate
from .study_link import StudyLinkCreate, StudyLink
from .site_has_study import SiteHasStudy
from .site import Site
from .study_external_id import StudyExternalIdCreate

from pydantic.utils import GetterDict

class StudySiteGetter(GetterDict):
    # map and reformat study fields
    def get(self, key: str, default: Any = None) -> Any:
        if key in ('id','name','create_date','city','state','zip'):
            return getattr(self._obj.site, key)
        else:
            return super(StudySiteGetter, self).get(key, default)

class StudySite(BaseModel):
    id: int
    name: Optional[str]
    country: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True
        getter_dict = StudySiteGetter

class StudyBase(BaseModel):
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]
    follow_up_info: Optional[str]

    class Config:
        orm_mode = True    

class Study(StudyBase):
    id: int
    links: List[StudyLink]
    sites: List[StudySite]

class StudyResults(BaseModel):
    version: Optional[str]
    studies: List[Study]

class StudyCreate(StudyBase):
    sites: Optional[List[SiteCreate]]
    links: Optional[List[StudyLinkCreate]]
    ext_ids: Optional[List[StudyExternalIdCreate]]

class StudySearchResults(BaseModel):
    results: Sequence[Study]

class StudyUpdates(BaseModel):
    source: str
    studies: Sequence[StudyCreate]
