from pydantic import BaseModel, Field, model_serializer
from datetime import datetime
from typing import Sequence, List, Optional
from gearbox.schemas import SiteCreate, Site, SiteHasStudySite
from .study_link import StudyLinkCreate, StudyLink
from .study_external_id import StudyExternalIdCreate

class StudyBase(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    create_date: Optional[datetime] = None
    active: Optional[bool] = None
    follow_up_info: Optional[str] = None

    class Config:
        from_attributes = True    

class Study(StudyBase):
    id: int
    links: Optional[List[StudyLink]] = None
    sites: Optional[List[SiteHasStudySite]] = None

    # The purpose of this function is to flatten
    # sites into the format expected for the studies extract
    @model_serializer()
    def serialize_model(self):

        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'create_date': self.create_date,
            'active': self.active,
            'follow_up_info': self.follow_up_info,
            'id': self.id, 
            'links': [{'name':s.name, 'href':s.href} for s in self.links], 
            'sites':[s.site for s in self.sites]
        }

    class Config:
        from_attributes = True    

class StudyBaseInfo(BaseModel):
    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    create_date: Optional[datetime] = None
    active: Optional[bool] = None

    class Config:
        from_attributes = True    

class StudyResults(BaseModel):
    version: Optional[str] = None
    studies: List[Study]

    class Config:
        from_attributes = True    
        

class StudyCreate(StudyBase):
    sites: Optional[List[SiteCreate]] = None
    links: Optional[List[StudyLinkCreate]] = None
    ext_ids: Optional[List[StudyExternalIdCreate]] = None

class StudySearchResults(BaseModel):
    results: Sequence[Study]

class StudyUpdates(BaseModel):
    source: str
    studies: Sequence[StudyCreate]
