from re import I
from gearbox import config
from datetime import date
from time import gmtime, strftime
from fastapi import APIRouter, HTTPException
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi import Request, Depends

from gearbox.services import eligibility_criteria as ec
from . import logger
from starlette.responses import JSONResponse 
from typing import List
from gearbox import auth
from gearbox.schemas import EligibilityCriteriaResponse
from gearbox import deps
from gearbox.util import bucket_utils, status
from gearbox.admin_login import admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/eligibility-criteria", dependencies=[Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_ec(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    params = []
    presigned_url = bucket_utils.get_presigned_url(request, config.S3_BUCKET_ELIGIBILITY_CRITERIA_KEY_NAME, params, "get_object")
    return JSONResponse(presigned_url, status.HTTP_200_OK) 

@mod.post("/build-eligibility-criteria", response_model=List[EligibilityCriteriaResponse], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=status.HTTP_200_OK)
async def build_eligibility_criteria(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    eligibility_criteria = await ec.get_eligibility_criteria(session)

    if not config.BYPASS_S3:
        params = [{'Content-Type':'application/json'}]
        bucket_utils.put_object(request, config.S3_BUCKET_NAME, config.S3_BUCKET_ELIGIBILITY_CRITERIA_KEY_NAME, config.S3_PUT_OBJECT_EXPIRES, params, eligibility_criteria)

    return JSONResponse(eligibility_criteria, status.HTTP_200_OK)


def init_app(app):
    app.include_router(mod, tags=["build_eligibility_criteria"])
    app.include_router(mod, tags=["eligibility_criteria"])
