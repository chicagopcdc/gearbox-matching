from __future__ import annotations
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError 
from pydantic import BaseModel, validator, Json
from datetime import datetime
from typing import Optional, List, Sequence, Any, Dict, Union

from gearbox.models import raw_criteria
 
# define the expected jsonschema schema for the algorithm logic
raw_criteria_schema = {
    "type":"object",
    "properties": {
        "id": {"type":"number"},
        "text": {"type":"string"},
        "nct": {"type":"string"},
        "pre-annotated": {"type":"array",
            "span":{"type":"array"
            },
            "matched-models":{"type":"array"
            }
        },
        "label": {"type":"array"},
        "comments": {"type":"array"}
    },       
    "required": ["id","text","nct"]
}       

class RawCriteriaBase(BaseModel):
    eligibility_criteria_id: int
    raw_criteria: Union[Json[Any],Dict] 

    @validator('raw_criteria')
    def check_valid_vs_schema(cls, v):
        
        try:
            # The validate method will throw a jsonschema.exceptions.ValidationError
            # if algorithm_logic field fails to validate against the algorithm_logic_schema
            validate(v, raw_criteria_schema)
        except ValidationError as e:
            # ValueError will be caught and handled by the app (in main.py)
            raise ValueError(f"ERROR VALIDATING raw_criteria: {e}")
        except Exception as e:
            # ValueError will be caught and handled by the app (in main.py)
            raise ValueError(f"ERROR VALIDATING raw_criteria: {e}")

        return v

    class Config:
        orm_mode = True    


class RawCriteria(RawCriteriaBase):
    id: int

class RawCriteriaSave(RawCriteriaBase):
    pass

class RawCriteriaCreate(RawCriteriaSave):
    pass 

class RawCriteriaUpdate(RawCriteriaSave):
    pass 

class RawCriteriaSearchResults(BaseModel):
    results: Sequence[RawCriteria]    
