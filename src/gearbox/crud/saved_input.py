from sqlalchemy import select, exc
from sqlalchemy.ext.asyncio import AsyncSession as Session
from gearbox.models import SavedInput
from gearbox.schemas import SavedInputCreate, SavedInputSearchResults
from fastapi import HTTPException
from gearbox.util import status
from .base import CRUDBase

from cdislogging import get_logger
logger = get_logger(__name__)

class CRUDSavedInput(CRUDBase [SavedInput, SavedInputCreate, SavedInputSearchResults]):

    async def get_all_saved_input(self, current_session: Session, logged_user_id: int):
        stmt = select(SavedInput).where(SavedInput.user_id==logged_user_id)
        result = await current_session.execute(stmt)
        saved_inputs = result.scalars().all()
        saved_inputs = [si.data for si in saved_inputs]
        return saved_inputs


    async def get_latest_saved_input(self, current_session: Session, user_id: int):
        stmt = select(SavedInput).where(SavedInput.user_id==user_id).order_by(SavedInput.create_date.desc())
        try:
            result = await current_session.execute(stmt)
            saved_input = result.scalars().first()
            return saved_input
        except exc.SQLAlchemyError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"SQL ERROR: {type(e)}")
    
saved_input_crud = CRUDSavedInput(SavedInput)