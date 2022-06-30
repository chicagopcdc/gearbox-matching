from pydantic import BaseModel, Field
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict

import logging
logger = logging.getLogger('gb-logger')

class Link(BaseModel):
    name: Optional[str]
    href: Optional[str]

class StudyResponse(BaseModel):
    id: int
    title: Optional[str]
    code: Optional[str]
    description: Optional[str]
    links: Optional[List[Link]]
    locations: Optional[List[str]]
