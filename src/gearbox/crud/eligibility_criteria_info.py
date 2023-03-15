from re import I
from telnetlib import EL
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session, joinedload, join
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from gearbox.util import status

from .base import CRUDBase
from gearbox.models import EligibilityCriteriaInfo
from gearbox.schemas import EligibilityCriteriaInfoSearchResults, EligibilityCriteriaInfoCreate

class CRUDEligibilityCriteriaInfo(CRUDBase [EligibilityCriteriaInfo, EligibilityCriteriaInfoCreate, EligibilityCriteriaInfoSearchResults]):
    ...

eligibility_criteria_info_crud = CRUDEligibilityCriteriaInfo(EligibilityCriteriaInfo)