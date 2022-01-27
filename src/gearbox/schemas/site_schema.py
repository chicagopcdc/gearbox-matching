from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict
# from .site_has_study import SiteStudy

class SiteStudyGetter(GetterDict):
    # map and reformat study fields
    def get(self, key: str, default: Any = None) -> Any:
        if key in ('id','name','code','description','create_date','active'):
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

    class Config:
        orm_mode = True
        getter_dict = SiteStudyGetter

class SiteSchema(BaseModel):
    id: int
    name: str
    code: str
    create_date: Optional[datetime]
    active: Optional[bool]
    studies: Optional[List[SiteStudy]]

    class Config:
        orm_mode = True

class SiteCreateSchema(BaseModel):
    pass

class SiteSearchResultsSchema(BaseModel):
    pass
