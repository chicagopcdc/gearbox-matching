from __future__ import annotations
import json
from jsonschema import validate
from pydantic import BaseModel, ValidationError, validator, Json
from datetime import datetime
from typing import Optional, List, Sequence, Any

from gearbox.models import study_algorithm_engine


algorithm_logic_schema = {
    "type":"object",
    "properties": {
        "studyId": {"type":"number"},
        "algorithm": {"$ref":"#/definitions/crit"},
    },  

    "definitions": {
        "crit": {
            "type":"object",
            "properties": {
                "operator": {"type":"string", "enum":["AND","OR"] },
                "criteria": {"type":"array",
                    "items": {          
                        "anyOf": [              
                            {"type":"number"},          
                            {"$ref":"#/definitions/crit"} 
                        ]                       
                    }                   
                }               
            }           
        }       
    }   
}


class StudyAlgorithmEngineBase(BaseModel):
    study_version_id: int
    start_date: Optional[datetime]
    algorithm_logic: Json[Any]
    algorithm_version: Optional[int]
    active: bool

    @validator('algorithm_logic')
    # note - first arg here is the class, the second is the field we are validating
    # pydantic validators return either an error or the validated field 
    def check_valid_json(cls, v):
        try:
            json.dumps(v)
        except ValueError as e: 
            raise ValidationError
        except Exception as e: 
            raise ValidationError
        return v

    @validator('algorithm_logic')
    def check_valid_vs_schema(cls, v):
        validation_errors =  validate(v, algorithm_logic_schema)
        if validation_errors:
            raise ValidationError(f"algorithm logic schema errors: {validation_errors}")

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