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
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    create_date: Optional[datetime] = None
    active: Optional[bool] = None
    create_date: Optional[datetime] = None
    active: Optional[bool] = None

    class Config:
        orm_mode = True
        getter_dict = SiteStudyGetter

class SiteBase(BaseModel):
    name: str
    country: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    create_date: Optional[datetime] = None

    class Config:
        orm_mode = True

class Site(SiteBase):
    id: int

class SiteCreate(SiteBase):
    pass

class SiteSearchResults(BaseModel):
    results: Sequence[Site]
