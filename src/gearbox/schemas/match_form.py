from xml.dom.minidom import Identified
from pydantic import BaseModel, Extra, Json, validator
from datetime import datetime
from typing import Optional, Sequence, List, Union, Dict, Any

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError 

# define the expected jsonschema schema for the showif logic
showif_logic_schema = {
    "type":"object",
    "properties": {
        "operator": {"type":"string", "enum":["AND","OR","eq","gt","gte","eq","lte","lt"] },
        "criteria": {"type":"array",
            "items": {
                "anyOf": [
                    {"type":"number"},
                    {"$ref":"#"}
                ]       
            }       
        }       
    },       
    "required": ["operator"]
}       

class MatchFormGroup(BaseModel):
    id: int
    name: str

class MatchFormOption(BaseModel):
    value: Union[float, int]
    label: str
    description: Optional[str]

class MatchFormField(BaseModel):
    id: int
    groupId: int
    name: str
    min: Optional[Union[float,int]] = None
    max: Optional[Union[float,int]] = None
    step: Optional[Union[float,int]] = None
    placeholder: Optional[str] = None
    label: str
    type: str
    options: Optional[List[MatchFormOption]] = None
    showIf: Optional[Union[Json[Any],Dict]]

    @validator('showIf')
    def check_valid_vs_logic_schema(cls, v):
        
        try:
            # The validate method will throw a jsonschema.exceptions.ValidationError
            # if showif_logic field fails to validate against the showif_logic_schema
            validate(v, showif_logic_schema)
        except ValidationError as e:
            # ValueError will be caught and handled by the app (in main.py)
            raise ValueError(f"ERROR VALIDATING showIf logic: {e}")
        except Exception as e:
            # ValueError will be caught and handled by the app (in main.py)
            raise ValueError(f"ERROR VALIDATING showIf logic: {e}")

        return v    

class MatchFormBase(BaseModel):
    groups: List[MatchFormGroup]
    fields: List[MatchFormField]

class MatchForm(MatchFormBase):
    pass