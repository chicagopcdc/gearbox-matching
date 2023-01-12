import json
from gearbox import config
from gearbox.util import status, bucket_utils
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

from gearbox import auth
from gearbox.admin_login import admin_required

from gearbox.schemas import StudyResponse
from gearbox.crud.study import get_single_study, get_studies
from gearbox import deps
from gearbox.util.study_response import format_study_response

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/study/{study_id}", response_model=List[StudyResponse], dependencies=[Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_study(
    request: Request,
    study_id: int,
    session: Session = Depends(deps.get_session)
):
    results = await get_single_study(session, study_id)
    study_response = format_study_response(results)
    return JSONResponse(study_response, status.HTTP_200_OK)

@mod.post("/build-studies", response_model=List[StudyResponse], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=status.HTTP_200_OK)
async def build_all_studies(
    request: Request,
    session: Session = Depends(deps.get_session)
):

    results = await get_studies(session)
    study_response = format_study_response(results)

    if not config.BYPASS_S3:
        params = [{'Content-Type':'application/json'}]
        bucket_utils.put_object(request, config.S3_BUCKET_NAME, config.S3_BUCKET_STUDIES_KEY_NAME, config.S3_PUT_OBJECT_EXPIRES, params, study_response)
    return JSONResponse(study_response, status.HTTP_200_OK)

@mod.get("/studies", dependencies=[ Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_all_studies(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    params = []
    presigned_url = bucket_utils.get_presigned_url(request, config.S3_BUCKET_STUDIES_KEY_NAME, params, "get_object")
    return JSONResponse(presigned_url, status.HTTP_200_OK)


def init_app(app):
    app.include_router(mod, tags=["study"])
    app.include_router(mod, tags=["build_studies"])
