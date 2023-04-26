import json
from gearbox import config
from gearbox.util import status, bucket_utils
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from fastapi import Request, Depends
from fastapi import APIRouter 
from . import logger
from starlette.responses import JSONResponse 

from gearbox import auth
from gearbox.admin_login import admin_required

from gearbox.schemas import StudyResponse, Study, StudyCreate, StudyResponseSearchResults
from gearbox import deps
from gearbox.util.study_response import format_study_response
from gearbox.services import study as study_service

mod = APIRouter()

@mod.get("/study/{study_id}", response_model=StudyResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate)] )
async def get_study(
    request: Request,
    study_id: int,
    session: AsyncSession = Depends(deps.get_session)
):
    results = await study_service.get_study_info(session, study_id)
    study_response = format_study_response(results)

    return study_response

@mod.post("/build-studies", response_model=StudyResponseSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)] )
async def build_all_studies(
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    results = await study_service.get_studies_info(session)
    study_response = format_study_response(results)

    if not config.BYPASS_S3:
        params = [{'Content-Type':'application/json'}]
        bucket_utils.put_object(request, config.S3_BUCKET_NAME, config.S3_BUCKET_STUDIES_KEY_NAME, config.S3_PUT_OBJECT_EXPIRES, params, study_response)

    return { "results": list(study_response) }

@mod.get("/studies", status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)] )
async def get_all_studies(
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    params = []
    presigned_url = bucket_utils.get_presigned_url(request, config.S3_BUCKET_STUDIES_KEY_NAME, params, "get_object")
    return JSONResponse(presigned_url, status.HTTP_200_OK)

@mod.post("/study", response_model=Study,status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: StudyCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    new_study = await study_service.create_study(session, body)
    await session.commit()
    return new_study

@mod.post("/update-study/{study_id}", response_model=Study, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    study_id: int,
    body: dict,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    upd_study = await study_service.update_study(session=session, study=body, study_id=study_id)
    return upd_study

def init_app(app):
    app.include_router(mod, tags=["study"])
    app.include_router(mod, tags=["build_studies"])
