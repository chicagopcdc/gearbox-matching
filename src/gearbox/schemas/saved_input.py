from pydantic import BaseModel
from datetime import date, datetime, time, timedelta
from typing import Sequence, List



class SavedInputBase(BaseModel):
    user_id: int
    patient_id: int
    data: str


# properties in DB
class SavedInputDB(SavedInputBase):
    id: int
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True


# properties to return to client
class SavedInput(SavedInputDB):
    pass


class SavedInputSearchResults(BaseModel):
    results: List[dict]
    id: int

class UploadSavedInput(BaseModel):
    data: List[dict]
    id: int = None