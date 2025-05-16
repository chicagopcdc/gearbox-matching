from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends, HTTPException, APIRouter

from . import logger
from gearbox.util import status
from gearbox.services import criterion as criterion_service
from gearbox.admin_login import admin_required

from gearbox.schemas import CriterionSearchResults, CriterionCreateIn, Criterion
from gearbox import deps
from gearbox import auth 
from gearbox.services.user_input import reset_user_validation_data

mod = APIRouter()

@mod.get("/criteria", response_model=CriterionSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def get_criteria(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    criteria = await criterion_service.get_criteria(session)
    return { "results" :criteria }

@mod.get("/criteria-not-exist-in-match-form", response_model=CriterionSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def get_criteria(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments: This endpoint returns all criteria in the criterion table that are currently 
    active but do not yet exist in the match_form. 
    """
    criteria = await criterion_service.get_criteria_not_exist_in_match_form(session)
    return { "results" : criteria }

@mod.get("/criterion/{criterion_id}", response_model=Criterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def get_criterion(
    criterion_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    criterion = await criterion_service.get_criterion(session=session, id=criterion_id)
    if not criterion:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
            f"criterion not found for id: {criterion_id}")
    else:
        return criterion

@mod.post("/criterion", response_model=Criterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: CriterionCreateIn,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):

    new_criterion = await criterion_service.create_new_criterion(session, body, user_id=int(user_id))
    await session.commit()
    reset_user_validation_data()
    return new_criterion

def init_app(app):
    app.include_router(mod, tags=["criterion"])