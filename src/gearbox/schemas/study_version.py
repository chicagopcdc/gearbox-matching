from urllib.request import HTTPDefaultErrorHandler
from pydantic import BaseModel 
from datetime import datetime
from typing import Sequence, List, Optional
from gearbox.schemas import StudyBaseInfo
from gearbox.util.types import StudyVersionStatus

class StudyVersionBase(BaseModel):
    study_id: int
    create_date: Optional[datetime]
    study_version_num: int
    eligibility_criteria_id: Optional[int]
    study_algorithm_engine_id: Optional[int]
    status: Optional[StudyVersionStatus]
    comments: Optional[str]

    class Config:
        orm_mode = True    

class StudyVersion(StudyVersionBase):
    id: int
    class Config:
        orm_mode = True

class StudyVersionCreate(BaseModel):
    study_id: int
    create_date: Optional[datetime]
    study_version_num: Optional[int]
    status: Optional[StudyVersionStatus]
    comments: Optional[str]

    class Config:
        orm_mode = True

class StudyVersionUpdate(BaseModel):
    id: int
    create_date: Optional[datetime]
    study_version_num: Optional[int]
    status: Optional[StudyVersionStatus]
    eligibility_criteria_id: Optional[int]
    study_algorithm_engine_id: Optional[int]

class StudyVersionInfo(StudyVersion):
    study: StudyBaseInfo

    class Config:
        orm_mode = True

class StudyVersionSearchResults(BaseModel):
    results: Sequence[StudyVersion]
