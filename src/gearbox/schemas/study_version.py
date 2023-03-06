from urllib.request import HTTPDefaultErrorHandler
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Sequence, List, Optional
from gearbox.schemas import StudyAlgorithmEngineCreate, StudyAlgorithmEngine

class StudyVersionBase(BaseModel):
    study_id: int
    create_date: Optional[datetime]
    study_version: int
    active: Optional[bool]

    class Config:
        orm_mode = True    

class StudyVersion(StudyVersionBase):
    id: int

class StudyVersionCreate(BaseModel):
    study_id: int
    create_date: Optional[datetime]
    active: Optional[bool]
    study_version: Optional[int]

    class Config:
        orm_mode = True

class StudyVersionSearchResults(BaseModel):
    results: Sequence[StudyVersion]