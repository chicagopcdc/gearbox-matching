from re import I
from pydantic import BaseModel, Extra
from datetime import datetime
from typing import Optional, Sequence

class EligibilityCriteriaInfoBase(BaseModel):
    create_date: Optional[datetime]
    active: Optional[bool]
    study_version_id: int
    study_algorithm_engine_id: int
    eligibility_criteria_id: int

    class Config:
        orm_mode = True   

class EligibilityCriteriaInfo(EligibilityCriteriaInfoBase):
    id: int

class EligibilityCriteriaInfoCreate(EligibilityCriteriaInfoBase):
    pass

class EligibilityCriteriaInfoSearchResults(BaseModel):
    results: Sequence[EligibilityCriteriaInfo]    