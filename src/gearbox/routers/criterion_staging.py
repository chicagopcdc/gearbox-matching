from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends
from typing import List
from . import logger
from gearbox.util import status
from gearbox.services import criterion_staging as criterion_staging_service
from gearbox.admin_login import admin_required

from gearbox.schemas import CriterionStagingCreate, CriterionStaging
from gearbox.crud import criterion_staging_crud
from gearbox import deps
from gearbox import auth 
from gearbox.services.user_input import reset_user_validation_data

mod = APIRouter()

@mod.get("/criterion-staging/{eligibility_criteria_id}", response_model=List[CriterionStaging], status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_staging_criterion_by_eligibility_criteria_id(
    eligibility_criteria_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    cs = await criterion_staging_service.get_criterion_staging_by_ec_id(session, eligibility_criteria_id)
    return cs

@mod.post("/update-criterion-staging", response_model=CriterionStaging, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    body: CriterionStaging,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    upd_value = await criterion_staging_service.update_criterion_staging(session=session, criterion=body)
    return upd_value


def init_app(app):
    app.include_router(mod, tags=["criterion-staging"])
