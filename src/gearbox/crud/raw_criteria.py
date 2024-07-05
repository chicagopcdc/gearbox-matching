from .base import CRUDBase
from gearbox.models import RawCriteria, EligibilityCriteria
from gearbox.schemas import RawCriteriaCreate, RawCriteriaSearchResults
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, update, select, exc

class CRUDRawCriteria(CRUDBase [RawCriteria, RawCriteriaCreate, RawCriteriaSearchResults]):

    ...

raw_criteria_crud = CRUDRawCriteria(RawCriteria)