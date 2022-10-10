import json
from .. import config
from ..util import status
from fastapi import APIRouter
from sqlalchemy.orm import Session
from datetime import date
from time import gmtime, strftime
from fastapi import Request, Depends
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from . import logger
from starlette.responses import JSONResponse 
from typing import List

from .. import auth
from ..admin_login import admin_required

from ..schemas import StudySchema, StudyResponse
from ..crud.study import get_single_study, get_studies
from .. import deps
from ..util.study_response import format_study_response

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/study/{study_id}", response_model=List[StudyResponse], dependencies=[Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_study(
    request: Request,
    study_id: int,
    session: Session = Depends(deps.get_session)
):
    auth_header = str(request.headers.get("Authorization", ""))
    results = await get_single_study(session, study_id)

    study_response = format_study_response(results)
    return JSONResponse(study_response, status.HTTP_200_OK)

# MAKE ADMIN ONLY
@mod.get("/build-studies", response_model=List[StudyResponse], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=status.HTTP_200_OK)
async def build_all_studies(
    request: Request,
    session: Session = Depends(deps.get_session)
):

    auth_header = str(request.headers.get("Authorization", ""))
    results = await get_studies(session)
    study_response = format_study_response(results)

    if not config.BYPASS_S3:
        params = [{'Content-Type':'application/json'}]
        try:
            request.app.boto_manager.put_object(config.S3_BUCKET_NAME, config.S3_BUCKET_STUDIES_KEY_NAME, 10, params, study_response) 
        except Exception as ex:
            raise HTTPException(status.get_starlette_status(ex.code), 
                detail="Error putting study object {} {}.".format(config.S3_BUCKET_NAME, ex))

    return JSONResponse(study_response, status.HTTP_200_OK)

@mod.get("/studies", dependencies=[ Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_all_studies(
    request: Request,
    session: Session = Depends(deps.get_session)
):

    try:
        study_response = request.app.boto_manager.presigned_url(config.S3_BUCKET_NAME,config.S3_BUCKET_STUDIES_KEY_NAME, "1800", {}, "get_object") 
    except Exception as ex:
        raise HTTPException(status.get_starlette_status(ex.code), 
            detail="Error fetching studies {} {}.".format(config.S3_BUCKET_NAME, ex))

    return JSONResponse(study_response, status.HTTP_200_OK)


def init_app(app):
    app.include_router(mod, tags=["study"])
    app.include_router(mod, tags=["build_studies"])
