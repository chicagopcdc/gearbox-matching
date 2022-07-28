from .. import config
import json, tempfile
##### TEMPORARY BOTO FOR TESTING ###
from pcdc_aws_client.boto import BotoManager
# from pcdc_aws_client.boto import BotoManager
from re import I
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import date
from time import gmtime, strftime
from sqlalchemy.orm import Session
from fastapi import Request, Depends, HTTPException
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from typing import List
from .. import auth
from ..schemas import AlgorithmEngine, AlgorithmResponse, StudyResponse
from ..crud.match_conditions import get_match_conditions
from .. import deps
from ..util import match_conditions as mc
from ..admin_login import admin_required

import logging
logger = logging.getLogger('gb-logger')

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/match-conditions", response_model=List[AlgorithmResponse], dependencies=[ Depends(auth.authenticate)], status_code=HTTP_200_OK)
async def get_mc(
    request: Request,
    session: Session = Depends(deps.get_session)
):

    AWS_REGION = "us-east-2"
    botomanager = BotoManager({'region_name': AWS_REGION}, logger)
    params = []

    try:
        match_conditions = botomanager.get_object(config.S3_BUCKET_NAME,config.S3_BUCKET_KEY_NAME, 300, params) 
        # match_conditions = botomanager.get_object(config.S3_BUCKET_NAME + "xxx",config.S3_BUCKET_KEY_NAME, 300, params) # FAIL
    except Exception as ex:
        raise HTTPException(get_starlette_status(ex.code), 
            detail="Error fetching match condition object {}.".format(config.S3_BUCKET_NAME))

    return JSONResponse(match_conditions, HTTP_200_OK)

def get_starlette_status(status):
    return {
        200: HTTP_200_OK,
        201: HTTP_201_CREATED,
        204: HTTP_204_NO_CONTENT,
        409: HTTP_409_CONFLICT,
        400: HTTP_400_BAD_REQUEST,
        401: HTTP_401_UNAUTHORIZED,
        403: HTTP_403_FORBIDDEN,
        404: HTTP_404_NOT_FOUND,
        500: HTTP_500_INTERNAL_SERVER_ERROR,
    }.get(status,HTTP_500_INTERNAL_SERVER_ERROR)

def init_app(app):
    app.include_router(mod, tags=["build_match_conditions"])
