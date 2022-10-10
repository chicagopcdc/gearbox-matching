from re import I
from .. import config
from pcdc_aws_client.boto import BotoManager
from datetime import date
from time import gmtime, strftime
from fastapi import APIRouter, HTTPException
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi import Request, Depends
from . import logger
from starlette.responses import JSONResponse 
from ..util import status
from typing import List
from .. import auth
from ..schemas import EligibilityCriteriaResponse
from .. import deps
from ..util import eligibility_criteria as ec
from ..admin_login import admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/eligibility-criteria", dependencies=[Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_ec(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    # get eligibility criteria from database if running locally
    if config.BYPASS_S3:
        eligibility_criteria = await ec.get_eligibility_criteria(session)
    else:
        try:
            botomanager = BotoManager({'region_name': config.AWS_REGION}, logger)
            eligibility_criteria = botomanager.presigned_url(config.S3_BUCKET_NAME,config.S3_BUCKET_ELIGIBILITY_CRITERIA_KEY_NAME, "1800", {}, "get_object") 
        except Exception as ex:
            raise HTTPException(status.get_starlette_status(ex.code), 
                detail="Error fetching eligibility criteria {} {}.".format(config.S3_BUCKET_NAME, ex))

    return JSONResponse(eligibility_criteria, status.HTTP_200_OK)

@mod.get("/build-eligibility-criteria", response_model=List[EligibilityCriteriaResponse], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=status.HTTP_200_OK)
async def build_eligibility_criteria(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    eligibility_criteria = await ec.get_eligibility_criteria(session)

    if not config.BYPASS_S3:
        botomanager = BotoManager({'region_name': config.AWS_REGION}, logger)
        params = [{'Content-Type':'application/json'}]
        try:
            # botomanager.put_object(config.S3_BUCKET_NAME, config.S3_BUCKET_ELIGIBILITY_CRITERIA_KEY_NAME, 10, params, eligibility_criteria) 
            botomanager.put_object("nobucket", config.S3_BUCKET_ELIGIBILITY_CRITERIA_KEY_NAME, 10, params, eligibility_criteria) 
        except Exception as ex:
            raise HTTPException(status.get_starlette_status(ex.code), 
                detail="Error putting eligibility criteria object {} {}.".format(config.S3_BUCKET_NAME, ex))

    return JSONResponse(eligibility_criteria, status.HTTP_200_OK)


def init_app(app):
    app.include_router(mod, tags=["build_eligibility_criteria"])
    app.include_router(mod, tags=["eligibility_criteria"])
