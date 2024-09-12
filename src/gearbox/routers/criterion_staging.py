from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Request, Depends
from typing import List
from gearbox.util import status
from gearbox.services import criterion_staging as criterion_staging_service
from gearbox.admin_login import admin_required

from gearbox.schemas import CriterionStaging, CriterionStagingUpdate, CriterionPublish, CriterionStagingCreate, CriterionStagingSearchResult
from gearbox import deps
from gearbox import auth 
from gearbox.util.types import AdjudicationStatus

mod = APIRouter()

@mod.get("/criterion-staging/{eligibility_criteria_id}", response_model=List[CriterionStagingSearchResult], status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
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
    upd_value = await criterion_staging_service.update(session=session, criterion=body, user_id=int(user_id))
    return upd_value

@mod.post("/criterion-staging-publish", status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def publish(
    body: CriterionPublish,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    """
    Comments: The purpose of this endpoint is to 'publish' a criterion_staging row into the 
    criterion table which makes it available to the match-form build. 
    """
    await criterion_staging_service.publish_criterion(session=session, criterion=body, user_id=int(user_id))

@mod.post("/criterion-staging", response_model=CriterionStaging, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: CriterionStagingCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    new_criterion_staging = await criterion_staging_service.create(session, body)
    await session.commit()
    return new_criterion_staging

@mod.post("/save-criterion-staging", response_model=CriterionStaging, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    body: CriterionStagingUpdate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    """
    Comments: this endpoint updates the criterion_staging row and sets the status to "IN_PROCESS"
    in order to allow the adjudicator to save changes before publishing the criterion to
    the match-form
    """

    body.criterion_adjudication_status = AdjudicationStatus.IN_PROCESS
    upd_value = await criterion_staging_service.update(session=session, criterion=body, user_id=int(user_id))
    return upd_value

@mod.post("/accept-criterion-staging/{criterion_staging_id}", response_model=CriterionStaging, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def accept_object(
    criterion_staging_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    """
    Comments: this endpoint updates the criterion_staging row and sets the status to "ACTIVE"
    for criterion that are identified as 'EXISTING' and are confirmed as existing
    by the adjudicator
    """

    # NEED TO CHECK THAT THE CURRENT STATUS IS 'EXISTING' BEFORE SETTING TO 'ACTIVE'

    # NEED TO CREATE AN UPDATE OBJECT WITH ONLY ID AND STATUS = 'ACTIVE'

    # body.criterion_adjudication_status = AdjudicationStatus.IN_PROCESS
    await criterion_staging_service.accept_criterion_staging(session=session , id=criterion_staging_id, user_id=user_id )

def init_app(app):
    app.include_router(mod, tags=["criterion-staging"])
