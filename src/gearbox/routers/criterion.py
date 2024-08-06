from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends

from . import logger
from gearbox.util import status
from gearbox.services import criterion as criterion_service
from gearbox.admin_login import admin_required

from gearbox.schemas import CriterionSearchResults, CriterionCreateIn, Criterion
from gearbox.crud import criterion_crud
from gearbox import deps
from gearbox import auth 
from gearbox.services.user_input import reset_user_validation_data

mod = APIRouter()

@mod.get("/criteria", response_model=CriterionSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_criteria(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    criteria = await criterion_service.get_criteria(session)
    return { "results" :list(criteria) }

@mod.get("/criterion/{criterion_id}", response_model=Criterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_criterion(
    criterion_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    criterion = await criterion_service.get_criterion(session=session, id=criterion_id)
    return criterion

@mod.get("/criterion/{criterion_status}", response_model=CriterionSearchResults, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate)])
async def get_criteria_by_status(
    criterion_status: str,
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    """
    Comments: Get all study versions with a given status
    """
    criteria = await criterion_service.get_criteria_by_status(session, criterion_status)
    return criteria

@mod.post("/criterion", response_model=Criterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: CriterionCreateIn,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):

    new_criterion = await criterion_service.create_new_criterion(session, body, user_id=user_id)
    await session.commit()
    reset_user_validation_data()
    return new_criterion

def init_app(app):
    app.include_router(mod, tags=["criterion"])