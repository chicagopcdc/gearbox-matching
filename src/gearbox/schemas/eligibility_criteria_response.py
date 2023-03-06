from pydantic import BaseModel
from typing import Sequence

class EligibilityCriteriaResponse(BaseModel):
    id: int
    fieldId: int
    fieldValue: float
    operator: str

class EligibilityCriteriaResponseResults(BaseModel):
    results: Sequence[EligibilityCriteriaResponse]    