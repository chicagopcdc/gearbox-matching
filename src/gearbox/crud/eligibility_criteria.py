from re import I
from telnetlib import EL
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session, joinedload, join
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from gearbox.models import ElCriteriaHasCriterion, Criterion, InputType

from fastapi import HTTPException
from gearbox.util import status

from .base import CRUDBase
from gearbox.models import EligibilityCriteria
from gearbox.schemas import EligibilityCriteriaSearchResults, EligibilityCriteriaCreate

class CRUDEligibilityCriteria(CRUDBase [EligibilityCriteria, EligibilityCriteriaCreate, EligibilityCriteriaSearchResults]):


    async def get_eligibility_criteria_info(self, current_session: Session):

        stmt = select(ElCriteriaHasCriterion).options(
            joinedload(ElCriteriaHasCriterion.criterion).options(
                joinedload(Criterion.input_type)
            ),
            joinedload(ElCriteriaHasCriterion.value)
        ).order_by(ElCriteriaHasCriterion.id)
        try:
            result = await current_session.execute(stmt)
            ec = result.unique().scalars().all()
            return ec
        except exc.SQLAlchemyError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")

eligibility_criteria_crud = CRUDEligibilityCriteria(EligibilityCriteria)