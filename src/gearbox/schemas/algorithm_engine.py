from __future__ import annotations
import json
from pydantic import BaseModel, ValidationError, validator, Json
from datetime import datetime
from typing import Optional, List, Sequence, Any

from gearbox.models import study_algorithm_engine

class AlgorithmEngineBase(BaseModel):
    study_algorithm_engine_id: int
    algorithm_engine_version: int
    algorithm_logic: Json[Any]
    active: bool

    #@validator('algorithm_logic')
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


class AlgorithmEngine(AlgorithmEngineBase):
    id: int
    study_algorithm_engine_id: int
    algorithm_engine_version: int
    active: bool

class AlgorithmEngineCreate(AlgorithmEngineBase):
    pass

class AlgorithmEngineUpdate(BaseModel):
    pass

class AlgorithmEngineSearchResults(BaseModel):
    results: Sequence[AlgorithmEngine]    

class AlgorithmResponse(BaseModel):
    operator: str
    criteria: int
    algorithm: List[AlgorithmResponse]

class AlgorithmEngine(BaseModel):
    pass

AlgorithmResponse.update_forward_refs()