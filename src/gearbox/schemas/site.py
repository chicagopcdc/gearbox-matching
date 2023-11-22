from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict
#from gearbox.schemas import StudyLink

class SiteStudyGetter(GetterDict):
    # map and reformat study fields
    def get(self, key: str, default: Any = None) -> Any:
        if key in ('id','name','code','description','create_date','active','links'):
            return getattr(self._obj.study, key)
        else:
            return super(SiteStudyGetter, self).get(key, default)

class SiteStudy(BaseModel):
    id: int
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]
#    links: Optional[List[StudyLink]]
    create_date: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True
        getter_dict = SiteStudyGetter

class SiteBase(BaseModel):
    name: str
    code: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True

class Site(SiteBase):
    id: int

class SiteCreate(SiteBase):
    pass

class SiteSearchResults(BaseModel):
    results: Sequence[Site]

"""
class SiteResponse(BaseModel):
    current_date: str
    current_time: str
    status: str
    body: List[Site]

    class Config:
        orm_mode = True
"""
