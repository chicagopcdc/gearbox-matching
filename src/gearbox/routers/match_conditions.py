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
from ..schemas import AlgorithmResponse 
from ..crud.match_conditions import get_algorithm_engines
from .. import deps
from ..util import match_conditions as mc, status, bucket_utils
from ..admin_login import admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/match-conditions", dependencies=[ Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_mc(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    params = []
    presigned_url = bucket_utils.get_presigned_url(request, config.S3_BUCKET_MATCH_CONDITIONS_KEY_NAME, params, "get_object")
    return JSONResponse(presigned_url, status.HTTP_200_OK) 

@mod.post("/build-match-conditions", response_model=List[AlgorithmResponse], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=status.HTTP_200_OK)
async def build_mc(
    request: Request,
    session: Session = Depends(deps.get_session)
):

    match_conditions = await mc.get_match_conditions(session)

    if not config.BYPASS_S3:
        params = [{'Content-Type':'application/json'}]
        bucket_utils.put_object(request, config.S3_BUCKET_NAME, config.S3_BUCKET_MATCH_CONDITIONS_KEY_NAME, config.S3_PUT_OBJECT_EXPIRES, params, match_conditions)
    return JSONResponse(match_conditions, status.HTTP_200_OK)

def init_app(app):
    app.include_router(mod, tags=["build_match_conditions"])
    app.include_router(mod, tags=["match_conditions"])
