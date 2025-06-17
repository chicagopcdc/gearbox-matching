from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional



class SavedInputBase(BaseModel):
    user_id: int
    name: str | None = ''
    patient_id: int | None = None
    data: List[dict]
    create_date: datetime | None = None
    update_date: datetime | None = None


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
    id: int | None = None
    name: str | None = ''

class SavedInputPost(SavedInputBase):
    id: int | None = None
    pass