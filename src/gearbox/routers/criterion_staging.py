from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Request, Depends
from typing import List
from gearbox.util import status
from gearbox.services import criterion_staging as criterion_staging_service
from gearbox.admin_login import admin_required

from gearbox.schemas import CriterionStaging, CriterionStagingUpdate
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.get("/criterion-staging/{eligibility_criteria_id}", response_model=List[CriterionStaging], status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_staging_criterion_by_eligibility_criteria_id(
    eligibility_criteria_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    cs = await criterion_staging_service.get_criterion_staging_by_ec_id(session, eligibility_criteria_id)
    if not cs:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"criterion-staging not found for id: {eligibility_criteria_id}")
    else:
        return cs

@mod.post("/update-criterion-staging", response_model=CriterionStaging, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    body: CriterionStagingUpdate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    """
    Comments:
    """
    await criterion_staging_service.update(session=session, criterion=body, user_id=user_id)


def init_app(app):
    app.include_router(mod, tags=["criterion-staging"])
