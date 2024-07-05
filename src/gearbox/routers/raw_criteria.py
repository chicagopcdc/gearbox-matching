from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends

from . import logger
from gearbox.util import status
from gearbox.services import raw_criteria as raw_criteria_service
from gearbox.admin_login import admin_required

from gearbox.schemas import RawCriteriaSearchResults, RawCriteriaCreate, RawCriteria
from gearbox.crud import raw_criteria_crud
from gearbox import deps
from gearbox import auth 
from gearbox.services.user_input import reset_user_validation_data

mod = APIRouter()

@mod.get("/raw_criteria", response_model=RawCriteriaSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_criteria(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    raw_criteria = await raw_criteria_service.get_criteria(session)
    return { "results" :list(raw_criteria) }

@mod.get("/raw_criteria/{raw_criteria_id}", response_model=RawCriteria, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_raw_criteria(
    raw_criteria_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    raw_criteria = await raw_criteria_service.get_raw_criteria(session=session, id=raw_criteria_id)
    return raw_criteria

@mod.get("/raw_criteria/{eligibility_criteria_status}", response_model=RawCriteriaSearchResults, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate)])
async def get_criteria_by_status(
    eligibility_criteria_status: str,
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    """
    Comments: Get all study versions with a given status
    """
    raw_criteria = await raw_criteria_service.get_raw_criteria_by_status(session, eligibility_criteria_status)
    return raw_criteria

@mod.post("/raw_criteria", response_model=RawCriteria, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: RawCriteriaCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    new_raw_criteria = await raw_criteria_service.create_new_raw_criteria(session, body)
    await session.commit()
    reset_user_validation_data()
    return new_raw_criteria

def init_app(app):
    app.include_router(mod, tags=["raw-criteria"])