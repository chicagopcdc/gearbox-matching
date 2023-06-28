from gearbox import config
from fastapi import APIRouter
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import Request, Depends

from gearbox.services import eligibility_criteria as ec
from . import logger
from starlette.responses import JSONResponse 
from typing import List
from gearbox import auth
from gearbox.schemas import EligibilityCriteriaResponseResults, EligibilityCriteriaSearchResults, EligibilityCriteria, EligibilityCriteriaCreate, EligibilityCriteriaResponse
from gearbox import deps
from gearbox.util import bucket_utils, status
from gearbox.admin_login import admin_required

mod = APIRouter()

# get eligibility-criteria set for the front end
@mod.get("/eligibility-criteria", dependencies=[Depends(auth.authenticate)] )
async def get_ec(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    params = []
    presigned_url = bucket_utils.get_presigned_url(request, config.S3_BUCKET_ELIGIBILITY_CRITERIA_KEY_NAME, params, "get_object")
    return JSONResponse(presigned_url, status.HTTP_200_OK) 

# get single eligibility-criteria set 
@mod.get("/eligibility-criteria/{ec_id}", dependencies=[Depends(auth.authenticate)] )
async def get_ec(
    ec_id: int,
    request: Request,
    session: Session = Depends(deps.get_session),
):
    params = []
    presigned_url = await ec.get_eligibility_criteria_set(session, id=ec_id)
    return JSONResponse(presigned_url, status.HTTP_200_OK) 

# build and return eligibility-criteria set for the front end
@mod.post("/build-eligibility-criteria", status_code=status.HTTP_200_OK, response_model=List[EligibilityCriteriaResponse], dependencies=[ Depends(auth.authenticate), Depends(admin_required)] )
async def build_eligibility_criteria(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    eligibility_criteria = await ec.get_eligibility_criteria_set(session)

    if not config.BYPASS_S3:
        params = [{'Content-Type':'application/json'}]
        bucket_utils.put_object(request, config.S3_BUCKET_NAME, config.S3_BUCKET_ELIGIBILITY_CRITERIA_KEY_NAME, config.S3_PUT_OBJECT_EXPIRES, params, eligibility_criteria)

    return eligibility_criteria

"""
@mod.get("/eligibility-criteria", response_model=EligibilityCriteriaSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_eligibility_criteria(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    eligibility_criteria = await ec.get_eligibility_criteria(session=session)
    return { "results" :list(eligibility_criteria) }
"""

@mod.post("/eligibility-criteria", response_model=EligibilityCriteria, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: EligibilityCriteriaCreate,
    request: Request,
    session: Session = Depends(deps.get_session),
):
    """
    Comments: This endpoint creates a row in the eligibility_criteria table that represents
    a set of el_criteria_has_criterions that are associated with a particular study version.
    """
    new_eligibility_criteria = await ec.create_eligibility_criteria(session=session)
    return new_eligibility_criteria

def init_app(app):
    app.include_router(mod, tags=["build_eligibility_criteria"])
    app.include_router(mod, tags=["eligibility_criteria"])