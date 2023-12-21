from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict

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
    create_date: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True
        getter_dict = SiteStudyGetter

class SiteBase(BaseModel):
    name: str
    code: Optional[str]
    country: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True

class Site(SiteBase):
    id: int

class SiteCreate(SiteBase):
    pass

class SiteSearchResults(BaseModel):
    results: Sequence[Site]
