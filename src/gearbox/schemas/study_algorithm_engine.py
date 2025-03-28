from __future__ import annotations
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError 
from pydantic import BaseModel, validator, Json
from datetime import datetime
from typing import Optional, List, Sequence, Any, Dict, Union

from gearbox.models import study_algorithm_engine

# define the expected jsonschema schema for the algorithm logic
algorithm_logic_schema = {
    "type":"object",
    "properties": {
        "operator": {"type":"string", "enum":["AND","OR"] },
        "criteria": {"type":"array",
            "items": {
                "anyOf": [
                    {"type":"number"},
                    {"$ref":"#"}
                ]       
            }       
        }       
    },       
    "required": ["criteria"]
}       

class StudyAlgorithmEngineBase(BaseModel):
    start_date: Optional[datetime]
    algorithm_logic: Union[Json[Any],Dict] 

    @validator('algorithm_logic')
    def check_valid_vs_schema(cls, v):
        
        try:
            # The validate method will throw a jsonschema.exceptions.ValidationError
            # if algorithm_logic field fails to validate against the algorithm_logic_schema
            validate(v, algorithm_logic_schema)
        except ValidationError as e:
            # ValueError will be caught and handled by the app (in main.py)
            raise ValueError(f"ERROR VALIDATING algorithm_logic: {e}")
        except Exception as e:
            # ValueError will be caught and handled by the app (in main.py)
            raise ValueError(f"ERROR VALIDATING algorithm_logic: {e}")

        return v

    class Config:
        orm_mode = True    


class StudyAlgorithmEngine(StudyAlgorithmEngineBase):
    id: int

class StudyAlgorithmEngineSave(StudyAlgorithmEngineBase):
    pass

class StudyAlgorithmEngineCreate(StudyAlgorithmEngineSave):
    study_version_id: int

class StudyAlgorithmEngineUpdate(StudyAlgorithmEngineSave):
    study_version_id: int
    id: int

class StudyAlgorithmEngineSearchResults(BaseModel):
    results: Sequence[StudyAlgorithmEngine]    
