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

mod = APIRouter()

@mod.get("/criteria", response_model=CriterionSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_criteria(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    criteria = await criterion_crud.get(session)
    return { "results" :list(criteria) }

@mod.get("/criterion/{criterion_id}", response_model=Criterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_criterion(
    criterion_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    criterion = await criterion_service.get_criterion(session=session, id=criterion_id)
    return criterion

@mod.post("/criterion", response_model=Criterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: CriterionCreateIn,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    new_criterion = await criterion_service.create_new_criterion(session, body)
    await session.commit()
    return new_criterion

def init_app(app):
    app.include_router(mod, tags=["criteria","criterion"])