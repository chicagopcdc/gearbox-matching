import json
from .. import config
from pcdc_aws_client.boto import BotoManager
import re
from datetime import date
from time import gmtime, strftime
from fastapi import APIRouter
from fastapi import APIRouter, Security
from sqlalchemy.orm import Session
from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer
from . import logger
from starlette.responses import JSONResponse 
from typing import List
from .. import auth
from ..schemas import DisplayRules 
from ..crud.match_form import get_form_info
from .. import deps
from ..util.bounds import bounds
from ..util import match_conditions as mc
from ..util import status
from ..util import match_form as mf
from ..admin_login import admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/build-match-form", response_model=List[DisplayRules], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=status.HTTP_200_OK)
async def build_match_info(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    match_form = await mf.get_match_form(session)

    if not config.BYPASS_S3:
        botomanager = BotoManager({'region_name': config.AWS_REGION}, logger)
        params = [{'Content-Type':'application/json'}]
        try:
            botomanager.put_object(config.S3_BUCKET_NAME, config.S3_BUCKET_MATCH_FORM_KEY_NAME, 10, params, match_form) 
        except Exception as ex:
            raise HTTPException(status.get_starlette_status(ex.code), 
                detail="Error putting match form object {}.".format(config.S3_BUCKET_NAME))

    return JSONResponse(match_form, status.HTTP_200_OK)

@mod.get("/match-form", dependencies=[ Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_match_form(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    params = []
    # build match form from database if running locally
    if config.BYPASS_S3:
        match_form = await mf.get_match_form(session)
    else:
        try:
            botomanager = BotoManager({'region_name': config.AWS_REGION}, logger)
            match_form = botomanager.presigned_url(config.S3_BUCKET_NAME,config.S3_BUCKET_MATCH_FORM_KEY_NAME, "1800", {}, "get_object") 
        except Exception as ex:
            raise HTTPException(status.get_starlette_status(ex.code), 
                detail="Error fetching match form {}.".format(config.S3_BUCKET_NAME))

    return JSONResponse(match_form, status.HTTP_200_OK)


def init_app(app):
    app.include_router(mod, tags=["build_match_form"])
    app.include_router(mod, tags=["match_form"])
