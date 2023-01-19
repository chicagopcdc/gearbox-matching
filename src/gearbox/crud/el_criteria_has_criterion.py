from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy import func, update, select, exc
from sqlalchemy.orm import Session, joinedload, join
from fastapi import HTTPException
from .base import CRUDBase
from gearbox.models import ElCriteriaHasCriterion
from gearbox.schemas import ElCriteriaHasCriterionSearchResults, ElCriteriaHasCriterionCreate
from gearbox.util import status

class CRUDElCriteriaHasCriterion(CRUDBase [ElCriteriaHasCriterion, ElCriteriaHasCriterionCreate, ElCriteriaHasCriterionSearchResults]):

        async def get_ids(self , current_session: Session, ec_id: int) -> List[int]:
            stmt = select(ElCriteriaHasCriterion).where(ElCriteriaHasCriterion.eligibility_criteria_id == ec_id).load_only(ElCriteriaHasCriterion.id)#ADD WHERE eligibility_criteria_id=???
            try:
                result_db = await current_session.execute(stmt)
                result = result_db.unique().scalars().all()
                return result
            except exc.SQLAlchemyError as e:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")

el_criteria_has_criterion_crud = CRUDElCriteriaHasCriterion(ElCriteriaHasCriterion)

