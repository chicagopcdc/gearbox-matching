from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List

class Note(BaseModel):
    pass

class NoteCreate(BaseModel):
    pass

class NoteSearchResults(BaseModel):
    pass
