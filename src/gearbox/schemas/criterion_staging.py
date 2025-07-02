from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from gearbox.util.types import AdjudicationStatus, EchcAdjudicationStatus
from gearbox.schemas import Value

class CriterionStagingBase(BaseModel):
    eligibility_criteria_id: int
    code: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    create_date: Optional[datetime] = None
    criterion_adjudication_status: AdjudicationStatus
    echc_adjudication_status: Optional[EchcAdjudicationStatus] = None
    ontology_code_id: Optional[int] = None
    input_type_id: Optional[int] = None

    start_char: int
    end_char: int
    text: str
    criterion_id: Optional[int] = None

    criterion_value_ids: Optional[List[int]] = None
    echc_value_ids: Optional[List[int]] = None
    echc_ids: Optional[List[int]] = None
    last_updated_by_user_id: Optional[int] = None

    class Config:
        orm_mode = True

class CriterionStaging(CriterionStagingBase):
    id: int

class CriterionStagingSearchResult(BaseModel):
    id: int
    criterion_value_list: Optional[List[Value]] = None

    eligibility_criteria_id: int
    code: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    create_date: Optional[datetime] = None
    criterion_adjudication_status: AdjudicationStatus
    echc_adjudication_status: Optional[EchcAdjudicationStatus] = None
    ontology_code_id: Optional[int] = None
    input_type_id: Optional[int] = None

    start_char: int
    end_char: int
    text: str
    criterion_id: Optional[int] = None
    last_updated_by_user_id: Optional[int] = None
    echc_value_ids: Optional[List[int]] = None
    echc_ids: Optional[List[int]] = None
    criterion_value_ids: Optional[List[int]] = None

class CriterionStagingUpdateIn(CriterionStagingBase):
    id: int
    start_char: Optional[int] = None
    end_char: Optional[int] = None
    text: Optional[str] = None
    eligibility_criteria_id: Optional[int] = None
    criterion_adjudication_status: Optional[AdjudicationStatus] = None
    echc_adjudication_status: Optional[EchcAdjudicationStatus] = None

class CriterionStagingUpdate(CriterionStagingUpdateIn):
    last_updated_by_user_id: Optional[int] = None

class CriterionStagingCreate(CriterionStagingBase):
    pass