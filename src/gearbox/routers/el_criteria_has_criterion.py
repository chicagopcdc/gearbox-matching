from fastapi import Depends

from collections.abc import Iterable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends
from . import logger
from gearbox.util import status
from gearbox.util.types import EchcAdjudicationStatus
from gearbox.admin_login import admin_required

from gearbox.schemas import ElCriteriaHasCriterionCreate, ElCriteriaHasCriterionSearchResults, ElCriteriaHasCriterion, ElCriteriaHasCriterions, CriterionStagingUpdate, ElCriteriaHasCriterionPublish
from gearbox.services import el_criteria_has_criterion as el_criteria_has_criterion_service, criterion_staging as criterion_staging_service
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.get("/el-criteria-has-criterions", response_model=ElCriteriaHasCriterionSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def get_el_criteria_has_criterions(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    el_criteria_has_criterions = await el_criteria_has_criterion_service.get_el_criteria_has_criterions(session=session)
    return { "results" :list(el_criteria_has_criterions) }

@mod.get("/el-criteria-has-criterions/{eligibility_criteria_id}", response_model=ElCriteriaHasCriterionSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def get_el_criteria_has_criterions(
    eligibility_criteria_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments: Fetch all el_criteria_has_criterion rows for a particular eligibility_criteria_id (study-version)
    """
    el_criteria_has_criterions = await el_criteria_has_criterion_service.get_el_criteria_has_criterions_by_ecid(session=session, ecid=eligibility_criteria_id)
    return { "results" :list(el_criteria_has_criterions) }

@mod.get("/el-criteria-has-criterion/{el_criteria_has_criterion_id}", response_model=ElCriteriaHasCriterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def get_el_criteria_has_criterion(
    el_criteria_has_criterion_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    ret_el_criteria_has_criterion = await el_criteria_has_criterion_service.get_el_criteria_has_criterion(session=session, id=el_criteria_has_criterion_id)
    return ret_el_criteria_has_criterion

@mod.post("/el-criteria-has-criterion", status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: ElCriteriaHasCriterionCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    """
    Comments: Save a row to the el_criteria_has_crition table
    """
    await el_criteria_has_criterion_service.create_el_criteria_has_criterion(session=session, el_criteria_has_criterion=body)

@mod.post("/update-el-criteria-has-criterion/{el_criteria_has_criterion_id}", response_model=ElCriteriaHasCriterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    el_criteria_has_criterion_id: int,
    body: dict,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments: Update el_criteria_has_criterion
    """
    upd_el_criteria_has_criterion = await el_criteria_has_criterion_service.update_el_criteria_has_criterion(session=session, el_criteria_has_criterion=body, el_criteria_has_criterion_id=el_criteria_has_criterion_id)
    return upd_el_criteria_has_criterion

@mod.post("/publish-el-criteria-has-criterion", response_model=ElCriteriaHasCriterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def publish(
    body: ElCriteriaHasCriterionPublish,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    """
    Comments: The purpose of this endpoint is to 'publish' a criterion_staging row into the 
    el_criteria_has_criterions table which stores study-related criteria along with 
    any associated values for eligibility. 
    """
    new_echc = await el_criteria_has_criterion_service.publish_echc(session=session, echc=body, user_id=int(user_id))
    return new_echc

def init_app(app):
    app.include_router(mod, tags=["el-criteria-has-criterion"])
