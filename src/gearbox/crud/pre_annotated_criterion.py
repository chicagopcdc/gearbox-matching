from .base import CRUDBase
from gearbox.models import PreAnnotatedCriterion
from gearbox.schemas import PreAnnotatedCriterionCreate, PreAnnotatedCriterionSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import delete, exc
from fastapi import HTTPException
from gearbox.util import status

from cdislogging import get_logger
logger = get_logger(__name__)

class CRUDPreAnnotatedCriterion(CRUDBase [PreAnnotatedCriterion, PreAnnotatedCriterionCreate, PreAnnotatedCriterionSearchResults]):

        async def clear_pre_annotated_by_id(self, current_session: Session, raw_criteria_id: int):

            try:
                stmt = delete(PreAnnotatedCriterion).where(PreAnnotatedCriterion.raw_criteria_id==raw_criteria_id)
                await current_session.execute(stmt)
            except exc.SQLAlchemyError as e:
                logger.error(f"Error clearing triggered_by and display_rules tables: {type(e)}")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}: {e}")

pre_annotated_criterion_crud = CRUDPreAnnotatedCriterion(PreAnnotatedCriterion)