from __future__ import annotations
from pydantic import BaseModel 
from datetime import datetime
from typing import Sequence, Optional
from gearbox.schemas import StudyBaseInfo
from gearbox.util.types import StudyVersionStatus

class StudyVersionBase(BaseModel):
    study_id: int
    create_date: Optional[datetime] = None
    study_version_num: int
    eligibility_criteria_id: Optional[int] = None
    study_algorithm_engine_id: Optional[int] = None
    status: Optional[StudyVersionStatus] = None
    comments: Optional[str] = None

    class Config:
        from_attributes = True 

class StudyVersion(StudyVersionBase):
    id: int
    class Config:
        from_attributes = True 

class StudyVersionCreate(BaseModel):
    study_id: int
    create_date: Optional[datetime] = None
    eligibility_criteria_id: Optional[int] = None
    study_version_num: Optional[int] = None
    status: Optional[StudyVersionStatus] = None
    comments: Optional[str] = None

    class Config:
        from_attributes = True 

class StudyVersionUpdate(BaseModel):
    id: int
    create_date: datetime | None = None
    study_version_num: int | None = None
    status: StudyVersionStatus | None = None
    eligibility_criteria_id: int | None = None
    study_algorithm_engine_id: int | None = None

class StudyVersionInfo(StudyVersion):
    study: StudyBaseInfo

    class Config:
        from_attributes = True 

class StudyVersionSearchResults(BaseModel):
    results: Sequence[StudyVersion]
