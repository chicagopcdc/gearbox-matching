from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from .input_type import InputType
from gearbox.util.types import CriterionStagingStatus

class CriterionStagingBase(BaseModel):
    eligibility_criteria_id: int
    input_id: Optional[str]
    code: Optional[str]
    display_name: Optional[str]
    description: Optional[str]
    create_date: Optional[datetime]
    status: Optional[CriterionStagingStatus]
    ontology_code_id: Optional[int]
    input_type_id: Optional[int]

    start_char: int
    end_char: int
    text: str
    criterion_id: Optional[int]

    tags: Optional[List[int]]
    values: Optional[List[int]]
    display_rules_priority: Optional[int]
    display_rules_version: Optional[int]
    triggered_by_criterion_id: Optional[int]
    triggered_by_values_id: Optional[int]
    triggered_by_path: Optional[str]

    class Config:
        orm_mode = True

class CriterionStaging(CriterionStagingBase):
    id: int

class CriterionStagingCreate(CriterionStagingBase):
    pass