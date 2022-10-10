from .. import config
from re import I
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import date
from time import gmtime, strftime
from sqlalchemy.orm import Session
from fastapi import Request, Depends, HTTPException
from . import config, logger
from starlette.responses import JSONResponse
from typing import List
from .. import auth
from ..schemas import AlgorithmEngine, AlgorithmResponse, StudyResponse
from ..crud.match_conditions import get_algorithm_engines
from .. import deps
from ..util import match_conditions as mc
from ..util import status
from ..admin_login import admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/match-conditions", dependencies=[ Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_mc(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    params = []

    try:
        match_conditions = request.app.boto_manager.presigned_url(config.S3_BUCKET_NAME,config.S3_BUCKET_MATCH_CONDITIONS_KEY_NAME, "1800", {}, "get_object") 
    except Exception as ex:
        raise HTTPException(status.get_starlette_status(ex.code), 
            detail="Error fetching match conditions {} {}.".format(config.S3_BUCKET_NAME, ex))

    return JSONResponse(match_conditions, status.HTTP_200_OK)

@mod.get("/build-match-conditions", response_model=List[AlgorithmResponse], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=status.HTTP_200_OK)
async def build_mc(
    request: Request,
    session: Session = Depends(deps.get_session)
):

    match_conditions = await mc.get_match_conditions(session)
    params = [{'Content-Type':'application/json'}]

    if not config.BYPASS_S3:
        try:
            request.app.boto_manager.put_object(config.S3_BUCKET_NAME, config.S3_BUCKET_MATCH_CONDITIONS_KEY_NAME, 10, params, match_conditions) 
        except Exception as ex:
            raise HTTPException(status.get_starlette_status(ex.code), 
                detail="Error putting match condition object {} {}.".format(config.S3_BUCKET_NAME, ex))
    
    return JSONResponse(match_conditions, status.HTTP_200_OK)

def init_app(app):
    app.include_router(mod, tags=["build_match_conditions"])
    app.include_router(mod, tags=["match_conditions"])
