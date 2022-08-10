from pydantic import BaseModel, Field
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict
from .study_link import StudyLink

class StudySiteGetter(GetterDict):
    # map and reformat site fields
    def get(self, key: str, default: Any = None) -> Any:
        # if key in ('id','code','name','create_date','active'):
        if key in ('name'):
            return getattr(self._obj.site, key)
        else:
            return super(StudySiteGetter, self).get(key, default)

class StudySite(BaseModel):
#    id: Optional[int]
#    code: Optional[str]
    name: Optional[str] 
#    create_date: Optional[datetime]
#    active: Optional[bool]
#    assoc_create_date: Optional[datetime]
#    assoc_active: Optional[bool]

    class Config:
        orm_mode = True
        getter_dict = StudySiteGetter

class StudySchema(BaseModel):
    id: int
    name: str
    code: str
    description: str
    create_date: Optional[datetime]
    active: Optional[bool]
    sites: Optional[List[StudySite]] = Field(alias="locations")
    links: Optional[List[StudyLink]]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class StudyCreateSchema(BaseModel):
    pass

class StudySearchResultsSchema(BaseModel):
    pass

class StudyResponse(BaseModel):
    current_date: str
    current_time: str
    status: str
    body: List[StudySchema]

    class Config:
        orm_mode = True
