from .. import config
import json, tempfile
from pcdc_aws_client.boto import BotoManager
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
from ..util import status
from ..admin_login import admin_required
import gearbox.config

from cdislogging import get_logger
logger = get_logger(__name__)

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/match-conditions", response_model=List[AlgorithmResponse], dependencies=[ Depends(auth.authenticate)], status_code=HTTP_200_OK)
async def get_mc(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    AWS_REGION = config.AWS_REGION
    botomanager = BotoManager({'region_name': AWS_REGION}, logger)
    params = []

    try:
        match_conditions = botomanager.get_object(config.S3_BUCKET_NAME,config.S3_BUCKET_KEY_NAME, 300, params) 
    except Exception as ex:
        raise HTTPException(status.get_starlette_status(ex.code), 
            detail="Error fetching match condition object {}.".format(config.S3_BUCKET_NAME))

    response = {
        "current_date": date.today().strftime("%B %d, %Y"),
        "current_time": strftime("%H:%M:%S +0000", gmtime()),
        "status": "OK",
        "body": match_conditions
    }
    return JSONResponse(response, HTTP_200_OK)

@mod.get("/build-match-conditions", response_model=List[AlgorithmResponse], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=HTTP_200_OK)
async def get_mc(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    all_algo_engs = await get_match_conditions(session)
    match_conditions = []
    ae_dict = {}

    for ae in all_algo_engs:
        if ae.study_algo_engine.study_version.study_id in ae_dict:
                ae_dict[ae.study_algo_engine.study_version.study_id].append((ae.path,ae.sequence))
        else:
            ae_dict[ae.study_algo_engine.study_version.study_id] = [(ae.path,ae.sequence)]

    for i in sorted(ae_dict):
        study_id = i
        paths = [ x[0] for x in sorted(ae_dict[i], key = lambda x: x[1])]
        match_conditions.append(mc.get_tree(paths, study_id=study_id))
    
    AWS_REGION = config.AWS_REGION
    botomanager = BotoManager({'region_name': AWS_REGION}, logger)
    params = [{'Content-Type':'application/json'}]

    try:
        botomanager.put_object(config.S3_BUCKET_NAME, config.S3_BUCKET_KEY_NAME, 10, params, match_conditions) 
    except Exception as ex:
        raise HTTPException(status.get_starlette_status(ex.code), 
            detail="Error fetching match condition object {}.".format(config.S3_BUCKET_NAME))
    
    response = {
        "current_date": date.today().strftime("%B %d, %Y"),
        "current_time": strftime("%H:%M:%S +0000", gmtime()),
        "status": "OK",
        "body": match_conditions
    }

    return JSONResponse(response, HTTP_200_OK)

def init_app(app):
    app.include_router(mod, tags=["build_match_conditions"])
    app.include_router(mod, tags=["match_conditions"])
