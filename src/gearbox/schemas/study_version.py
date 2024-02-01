from urllib.request import HTTPDefaultErrorHandler
from pydantic import BaseModel 
from datetime import datetime
from typing import Sequence, List, Optional
from gearbox.schemas import EligibilityCriteriaInfo, Study

class StudyVersionBase(BaseModel):
    study_id: int
    create_date: Optional[datetime]
    study_version_num: int
    active: Optional[bool]

    class Config:
        orm_mode = True    

class StudyVersion(StudyVersionBase):
    id: int
    class Config:
        orm_mode = True

class StudyVersionCreate(BaseModel):
    study_id: int
    create_date: Optional[datetime]
    active: Optional[bool]
    study_version_num: Optional[int]

    class Config:
        orm_mode = True

class StudyVersionInfo(StudyVersion):
    eligibility_criteria_infos: List[EligibilityCriteriaInfo]
    study: Study

    class Config:
        orm_mode = True

class StudyVersionSearchResults(BaseModel):
    results: Sequence[StudyVersion]