from fastapi import Depends

from collections.abc import Iterable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends
from . import logger
from gearbox.util import status
from gearbox.admin_login import admin_required

from gearbox.schemas import ElCriteriaHasCriterionCreate, ElCriteriaHasCriterionSearchResults, ElCriteriaHasCriterion
from gearbox.services import el_criteria_has_criterion as el_criteria_has_criterion_service
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.get("/el-criteria-has-criterions", response_model=ElCriteriaHasCriterionSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_el_criteria_has_criterions(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    el_criteria_has_criterions = await el_criteria_has_criterion_service.get_el_criteria_has_criterions(session=session)
    return { "results" :list(el_criteria_has_criterions) }

@mod.get("/el-criteria-has-criterion/{el_criteria_has_criterion_id}", response_model=ElCriteriaHasCriterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_el_criteria_has_criterion(
    el_criteria_has_criterion_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    ret_el_criteria_has_criterion = await el_criteria_has_criterion_service.get_el_criteria_has_criterion(session=session, id=el_criteria_has_criterion_id)
    return ret_el_criteria_has_criterion

@mod.post("/el-criteria-has-criterion", response_model=ElCriteriaHasCriterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: ElCriteriaHasCriterionCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    new_el_criteria_has_criterion = await el_criteria_has_criterion_service.create_el_criteria_has_criterion(session=session, el_criteria_has_criterion=body)
    return new_el_criteria_has_criterion

@mod.post("/update-el-criteria-has-criterion/{el_criteria_has_criterion_id}", response_model=ElCriteriaHasCriterion, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    el_criteria_has_criterion_id: int,
    body: dict,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    upd_el_criteria_has_criterion = await el_criteria_has_criterion_service.update_el_criteria_has_criterion(session=session, el_criteria_has_criterion=body, el_criteria_has_criterion_id=el_criteria_has_criterion_id)
    return upd_el_criteria_has_criterion

def init_app(app):
    app.include_router(mod, tags=["el_criteria_has_criterion","el_criteria_has_criterions","update-el_criteria_has_criterion"])
