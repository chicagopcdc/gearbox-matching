from datetime import datetime
from typing import List, Any
from pydantic import BaseModel
from pydantic.utils import GetterDict

class SiteStudyGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in ('id','name','code','description','create_date','active'):
            return getattr(self._obj.study, key)
        else:
            return super(SiteStudyGetter, self).get(key, default)

class SiteStudy(BaseModel):
    id: int
    name: str
    code: str
    description: str
    create_date: datetime
    active: bool

    class Config:
        orm_mode = True
        getter_dict = SiteStudyGetter

class StudySiteGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in ('id','name','code','create_date','active'):
            return getattr(self._obj.site, key)
        else:
            return super(StudySiteGetter, self).get(key, default)

class StudySite(BaseModel):
    id: int
    name: str
    code: str
    create_date: datetime
    active: bool

    class Config:
        orm_mode = True
        getter_dict = StudySiteGetter