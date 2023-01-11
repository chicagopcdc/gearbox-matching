from pydantic import BaseModel
from datetime import datetime

class EligibilityCriteriaResponse(BaseModel):
    id: int
    fieldId: int
    fieldValue: int
    operator: str