#from urllib.request import HTTPDefaultErrorHandler
from pydantic import BaseModel #, HttpUrl
from datetime import datetime
from typing import Sequence, List, Optional, Any
from gearbox.schemas import SiteCreate #, StudyLinkCreate
from .study_link import StudyLinkCreate, StudyLink
from .site_has_study import SiteHasStudy
from .site import Site

from pydantic.utils import GetterDict

class StudySiteGetter(GetterDict):
    # map and reformat study fields
    def get(self, key: str, default: Any = None) -> Any:
        if key in ('id','name','code','create_date','active'):
            return getattr(self._obj.site, key)
        else:
            return super(StudySiteGetter, self).get(key, default)

class StudySite(BaseModel):
    id: int
    name: Optional[str]
    code: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True
        getter_dict = StudySiteGetter

class StudyBase(BaseModel):
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True    

class Study(StudyBase):
    id: int
    links: List[StudyLink]
    sites: List[StudySite]


class StudyCreate(StudyBase):
    sites: Optional[List[SiteCreate]]
    links: Optional[List[StudyLinkCreate]]

class StudySearchResults(BaseModel):
    results: Sequence[Study]

"""
class StudyCreateFull(StudyBase):
    sites: Optional [Sequence[SiteCreate]]
    study_links: Optional [Sequence[StudyLinkCreate]]
    study_version: Optional[StudyVersionCreate]
    study_algorithm_engine: Optional[StudyAlgorithmEngineCreate]
"""