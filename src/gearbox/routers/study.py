from gearbox import config
from gearbox.util import status, bucket_utils
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends, APIRouter, HTTPException
from . import logger
from starlette.responses import JSONResponse 

from gearbox import auth
from gearbox.admin_login import admin_required, super_admin_required

from gearbox.schemas import Study, StudyCreate, StudyUpdates, StudyResults 
from gearbox import deps
from gearbox.services import study as study_service
from fastapi.encoders import jsonable_encoder

mod = APIRouter()

@mod.get("/study/{study_id}", response_model=Study, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate), Depends(admin_required)] )
async def get_study(
    request: Request,
    study_id: int,
    session: AsyncSession = Depends(deps.get_session)
):
    study = await study_service.get_study_info(session, study_id)
    if not study:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
            f"study not found for study id: {study_id}")
    else:
        return study 

@mod.post("/build-studies", response_model=StudyResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(super_admin_required)] )
async def build_all_studies(
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    new_studies = await study_service.build_studies(session=session, request=request)
    return new_studies

@mod.get("/studies", status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)] )
async def get_all_studies(
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    """
    Comments: This endpoint is called by the front-end to return the presigned_url to the S3
    bucket that contains the study file
    """
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

@mod.post("/update-studies", status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_studies(
    body: StudyUpdates,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments: This endpoint does a refresh of the study, study_links, study_external_ids,
        site_has_study, and site tables. Rather than delete the existing information,
        the 'active' flag is set to false for all studies that do not exist in the
        studyupdates json document.
    """
    await study_service.update_studies(session=session, request=request, updates=body)

    return JSONResponse(status.HTTP_200_OK)

def init_app(app):
    app.include_router(mod, tags=["study"])
