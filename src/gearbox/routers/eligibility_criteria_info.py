from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends
from fastapi import APIRouter 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import date
from . import logger
from typing import List
from ..util import status
from gearbox import auth
from gearbox.schemas import EligibilityCriteriaInfoSearchResults, EligibilityCriteriaInfo as EligibilityCriteriaInfoSchema, EligibilityCriteriaInfoCreate
from gearbox import deps
from gearbox.services import eligibility_criteria_info  as eligibility_criteria_info_service
from gearbox.services import eligibility_criteria_info  as eligibility_criteria_info_service
from gearbox.admin_login import admin_required

mod = APIRouter()

# ADD ROUTER TO FETCH ALL eligibility_criteria_info FOR A GIVEN STUDY
# THIS IS FOR THE FE TO MATCH study_algorithm_engines TO study_versions
# AND eligibility_criteria - ENDPOINT SHOULD RETURN:
# study, study_version, eligibility_criteria, all el_criteria_has_criterion ROWS
# (and study_algorithm_engine data if exists)

@mod.get("/eligibility-criteria-info/{eligibility_criteria_info_id}", response_model=EligibilityCriteriaInfoSchema, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate)] )
async def get_eligibility_criteria_info(
    request: Request,
    eligibility_criteria_info_id: int,
    session: AsyncSession = Depends(deps.get_session),
):
    ret_eligibility_criteria_info = await eligibility_criteria_info_service.get_eligibility_criteria_info(session, eligibility_criteria_info_id)
    return ret_eligibility_criteria_info

@mod.get("/eligibility-criteria-infos", response_model=List[EligibilityCriteriaInfoSchema], status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate)])
async def get_all_eligibility_criteria_infos(
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    eligibility_criteria_infos = await eligibility_criteria_info_service.get_eligibility_criteria_infos(session)
    return eligibility_criteria_infos

@mod.post("/eligibility-criteria-info", response_model=EligibilityCriteriaInfoSchema, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: EligibilityCriteriaInfoCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    new_eligibility_criteria_info = await eligibility_criteria_info_service.create_eligibility_criteria_info(session, body)
    await session.commit()
    return new_eligibility_criteria_info

@mod.post("/update-eligibility-criteria-info/{eligibility_criteria_info_id}", response_model=EligibilityCriteriaInfoSchema, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    eligibility_criteria_info_id: int,
    body: dict,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    upd_eligibility_criteria_info = await eligibility_criteria_info_service.update_eligibility_criteria_info(session=session, eligibility_criteria_info=body, eligibility_criteria_info_id=eligibility_criteria_info_id)
    return upd_eligibility_criteria_info

def init_app(app):
    app.include_router(mod, tags=["eligibility-criteria-info"])
