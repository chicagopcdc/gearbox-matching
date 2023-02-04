from __future__ import annotations
import json
from jsonschema import validate
from pydantic import BaseModel, ValidationError, validator, Json
from datetime import datetime
from typing import Optional, List, Sequence, Any
import jsonschema

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


class AlgorithmEngineBase(BaseModel):
    study_algorithm_engine_id: int
    algorithm_engine_version: int
    algorithm_logic: Json[Any]
    active: bool

    @validator('algorithm_logic')
    # note - first arg here is the class, the second is the field we are validating
    # pydantic validators return either an error or the validated field 
    def check_valid_json(cls, v):
        print("HERE IN FIRST VALIDATOR**********************************")
        try:
            json.loads(v)
        except ValueError: 
            raise ValidationError('algorithm logic not valid json')
        return v

    @validator('algorithm_logic')
    def check_valid_json(cls, v):
        print("HERE IN VALIDATOR**********************************")
        validation_errors =  validate(v, algorithm_logic_schema)
        if validation_errors:
            raise ValidationError(f"algorithm logic schema errors: {validation_errors}")
    


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