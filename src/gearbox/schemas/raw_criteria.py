from __future__ import annotations
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError 
from pydantic import BaseModel, validator, Json, root_validator
from datetime import datetime
from typing import Optional, List, Sequence, Any, Dict, Union

from gearbox.models import raw_criteria
 
# define the expected jsonschema schema for the raw criteria 
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
    data: Union[Json[Any],Dict] 

    @validator('data')
    def check_valid_vs_schema(cls, v):
        try:
            # The validate method will throw a jsonschema.exceptions.ValidationError
            # if raw_criteria fails to validate against the raw criteria schema 
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
    eligibility_criteria_id: int

class RawCriteriaIn(RawCriteriaBase):
    pass 

class RawCriteriaCreate(RawCriteriaBase):
    eligibility_criteria_id: int
    pass 

class RawCriteriaUpdate(RawCriteriaBase):
    pass 

#class RawCriteriaSearchResults(BaseModel):
#    results: Sequence[RawCriteria]    
