from __future__ import annotations
import json
from pydantic import BaseModel, ValidationError, validator, Json
from datetime import datetime
from typing import Optional, List, Sequence, Any

from gearbox.models import study_algorithm_engine

class StudyAlgorithmEngineBase(BaseModel):
    study_version_id: int
    start_date: Optional[datetime]
    algorithm_logic: Json[Any]
    algorithm_version: Optional[int]
    active: bool

    # @validator('algorithm_logic')
    # note - first arg here is the class, the second is the field we are validating
    # pydantic validators return either an error or the validated field 
    #def check_valid_json(cls, v):
    #    try:
    #        json.loads(v)
    #    except ValueError: 
    #        raise ValidationError
    #    return v


    class Config:
        orm_mode = True    


class StudyAlgorithmEngine(StudyAlgorithmEngineBase):
    id: int

class StudyAlgorithmEngineCreate(StudyAlgorithmEngineBase):
    pass

class StudyAlgorithmEngineUpdate(BaseModel):
    pass

class StudyAlgorithmEngineSearchResults(BaseModel):
    results: Sequence[StudyAlgorithmEngine]    

"""
class StudyAlgorithmResponse(BaseModel):
    operator: str
    criteria: int
    algorithm: List[StudyAlgorithmResponse]

class StudyAlgorithmEngine(BaseModel):
    pass

StudyAlgorithmResponse.update_forward_refs()
"""