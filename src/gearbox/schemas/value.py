from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List

# from gearbox.schemas.el_criterion_has_criterion_schema import ElCriterionHasCriterionSchema

class Value(BaseModel):
    id: int
    code: str
    description: str
    type: str
    value_string: str
    unit: str
    operator: str
    create_date: datetime
    active: bool
    # el_criteria_has_criterions: List[ElCriterionHasCriterionSchema]


class ValueCreate(BaseModel):
    pass

class ValueSearchResults(BaseModel):
    pass
