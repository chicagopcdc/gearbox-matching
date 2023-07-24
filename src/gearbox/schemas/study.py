#from urllib.request import HTTPDefaultErrorHandler
from pydantic import BaseModel #, HttpUrl
from datetime import datetime
from typing import Sequence, List, Optional
from gearbox.schemas import SiteCreate #, StudyLinkCreate
from .study_link import StudyLinkCreate, StudyLink
from .site import Site, SiteStudy

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
    sites: List[SiteStudy]
    links: List[StudyLink]

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