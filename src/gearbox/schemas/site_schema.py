from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict
from .study_link import StudyLink
from .. import logger

class SiteStudyGetter(GetterDict):
    # map and reformat study fields
    def get(self, key: str, default: Any = None) -> Any:
        logger.info(f" {key} HERE IN site_schema.py!!!!!!!!!******************************************************")
        if key in ('id','name','code','description','create_date','active','links'):
        # if key in ('id','name','code','description','create_date','active'):
            logger.info(f"KEY: {key} VALUE: {getattr(self._obj.study, key)}")
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
    links: Optional[List[StudyLink]]
    assoc_create_date: Optional[datetime]
    assoc_active: Optional[bool]

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
