from xml.dom.minidom import Identified
from pydantic import BaseModel, Extra, Json, validator
from datetime import datetime
from typing import Optional, Sequence, List, Union, Dict, Any

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError 

match_form_group_schema = {
    "type":"array",
    "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"}
        },
    "required": ["id","name"]
}

#        "fields": {"type:":"array",
#            "id": {"type": "number"},
#            "groupId": {"type": "number"},
#            "name": {"type": "string"},
#            "label": {"type": "string"},
#            "type": {"type": "string"},
#            "options": {"type:":"array",
#                "value": {"type": "number"},
#                "label": {"type": "string"},
#                "description": {"type": "string"}
#            },
#            "showIf": {"type:":"array",
#                "operator": {"type":"string", "enum":["AND","OR"] },
#                "criteria": {"type":"array",
#                "items": {
#                    "anyOf": [
#                        {"type":"number"},
#                        {"$ref":"#"}
#                    ]       
#                }          
#                }       
#            }
#        }
#    },       
#    "required": ["groups","fields"]
#}       

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

class MatchFormBase(BaseModel):
    groups: List[MatchFormGroup]
    fields: List[MatchFormField]

    @validator('groups')
    def check_valid_vs_groups_schema(cls, v):
        
        try:
            # The validate method will throw a jsonschema.exceptions.ValidationError
            # if algorithm_logic field fails to validate against the algorithm_logic_schema
            validate(v, match_form_group_schema)
        except ValidationError as e:
            # ValueError will be caught and handled by the app (in main.py)
            raise ValueError(f"ERROR VALIDATING match form groups: {e}")
        except Exception as e:
            # ValueError will be caught and handled by the app (in main.py)
            raise ValueError(f"ERROR VALIDATING match form groups: {e}")

        return v    

class MatchForm(MatchFormBase):
    pass