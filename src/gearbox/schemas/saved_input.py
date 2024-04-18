from pydantic import BaseModel
from datetime import date, datetime, time, timedelta
from typing import Sequence, List, Optional



class SavedInputBase(BaseModel):
    user_id: int
    name: Optional[str]
    patient_id: Optional[int]
    data: List[dict]
    create_date: Optional[datetime]
    update_date: Optional[datetime]


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
    name: Optional[str]

class SavedInputCreate(BaseModel):
    data: List[dict]
    id: Optional[int]
    name: Optional[str]

class SavedInputPost(SavedInputBase):
    id: Optional[int]
    pass