from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from .input_type import InputType
from gearbox.util.types import AdjudicationStatus, EchcAdjudicationStatus
from gearbox.schemas import Value

class CriterionStagingBase(BaseModel):
    eligibility_criteria_id: int
    input_id: Optional[str] = ""
    code: Optional[str] = ""
    display_name: Optional[str] = ""
    description: Optional[str] = ""
    create_date: Optional[datetime] = ""
    criterion_adjudication_status: AdjudicationStatus
    echc_adjudication_status: Optional[EchcAdjudicationStatus]
    ontology_code_id: Optional[int]
    input_type_id: Optional[int]

    start_char: int
    end_char: int
    text: str
    criterion_id: Optional[int]

    criterion_value_ids: Optional[List[int]] = []
    echc_value_ids: Optional[List[int]] = []
    echc_ids: Optional[List[int]] = []
    last_updated_by_user_id: Optional[int]

    class Config:
        orm_mode = True

class CriterionStaging(CriterionStagingBase):
    id: int

class CriterionStagingSearchResult(BaseModel):
    id: int
    criterion_value_list: Optional[List[Value]]

    eligibility_criteria_id: int
    input_id: Optional[str] = ""
    code: Optional[str] = ""
    display_name: Optional[str] = ""
    description: Optional[str] = ""
    create_date: Optional[datetime] = ""
    criterion_adjudication_status: AdjudicationStatus
    echc_adjudication_status: Optional[EchcAdjudicationStatus]
    ontology_code_id: Optional[int]
    input_type_id: Optional[int]

    start_char: int
    end_char: int
    text: str
    criterion_id: Optional[int]
    last_updated_by_user_id: Optional[int]
    echc_value_ids: Optional[List[int]] = []
    echc_ids: Optional[List[int]] = []
    criterion_value_ids: Optional[List[int]] = []

class CriterionStagingUpdateIn(CriterionStagingBase):
    id: int
    start_char: Optional[int]
    end_char: Optional[int]
    text: Optional[str]
    eligibility_criteria_id: Optional[int]
    criterion_adjudication_status: Optional[AdjudicationStatus]
    echc_adjudication_status: Optional[EchcAdjudicationStatus]

class CriterionStagingUpdate(CriterionStagingUpdateIn):
    last_updated_by_user_id: Optional[int]

class CriterionStagingCreate(CriterionStagingBase):
    pass