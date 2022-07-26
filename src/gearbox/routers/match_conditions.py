import json, tempfile
from .boto_temp import BotoManager
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

@mod.get("/match-conditions", response_model=List[AlgorithmResponse], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=HTTP_200_OK)
async def get_mc(
    request: Request,
    session: Session = Depends(deps.get_session)
):

    AWS_REGION = "us-east-2"
    botomanager = BotoManager({'region_name': AWS_REGION}, logger)
    params = []

    # create and upload match conditions from a temporary file
    try:
        # def get_object(self, bucket, key, expires, config):
        match_conditions = botomanager.get_object('gearbox-match-conditions-bucket','mc.json', 300, params) 
    except Exception as ex:
            print(f"GET EXCEPTION: {ex}")
        
    response = {
        "current_date": date.today().strftime("%B %d, %Y"),
        "current_time": strftime("%H:%M:%S +0000", gmtime()),
        "status": "OK",
        "body": match_conditions
    }
    
    return JSONResponse(response, HTTP_200_OK)

def init_app(app):
    app.include_router(mod, tags=["build_match_conditions"])
