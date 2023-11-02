from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict
# import json
from sqlalchemy import JSON

class StudyHasPatientBase(BaseModel):
    study_id: int
    patient_id: str
    data: Any
    source_id: str

    class Config:
        orm_mode = True

class StudyHasPatient(StudyHasPatientBase):
    pass

class StudyHasPatientCreate(BaseModel):
    shps: Sequence[StudyHasPatientBase]

class StudyHasPatientSearchResults(StudyHasPatientBase):
    results: Sequence[StudyHasPatient]