from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends, APIRouter, HTTPException
from . import logger
from ..util import status
from typing import List
from gearbox import auth
from gearbox.schemas import StudyVersionUpdate, StudyVersion as StudyVersionSchema, StudyVersionCreate, StudyVersionInfo
from gearbox import deps
from gearbox.services import study_version  as study_version_service
from gearbox.admin_login import admin_required

mod = APIRouter()

@mod.get("/study-version/{study_version_id}", response_model=StudyVersionInfo, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate), Depends(admin_required)] )
async def get_study_version(
    request: Request,
    study_version_id: int,
    session: AsyncSession = Depends(deps.get_session),
):
    ret_study_version = await study_version_service.get_study_version(session, study_version_id)
    if not ret_study_version:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
            f"study_version not found for id: {study_version_id}")
    else:
        return ret_study_version

@mod.get("/study-versions", response_model=List[StudyVersionInfo], status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate), Depends(admin_required)])
async def get_all_study_versions(
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    study_versions = await study_version_service.get_study_versions(session)
    return study_versions

@mod.get("/study-versions-adjudication", response_model=List[StudyVersionInfo], status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate), Depends(admin_required)])
async def get_all_study_versions(
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    study_versions = await study_version_service.get_study_versions_for_adjudication(session)
    if not study_versions:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
            f"no study_versions found requireing adjudication")
    else:
        return study_versions

@mod.get("/study-versions/{study_version_status}", response_model=List[StudyVersionInfo], status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate), Depends(admin_required)])
async def get_study_versions(
    study_version_status: str,
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    """
    Comments: Get all study versions with a given status
    """
    study_versions = await study_version_service.get_study_versions_by_status(session, study_version_status)
    if not study_versions:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
            f"study_versions not found for status: {study_version_status}")
    else:
        return study_versions

@mod.post("/study-version", response_model=StudyVersionSchema, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: StudyVersionCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    new_study_version = await study_version_service.create_study_version(session, body)
    await session.commit()
    return new_study_version

@mod.post("/update-study-version", response_model=StudyVersionSchema, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    body: StudyVersionUpdate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    upd_study_version = await study_version_service.update_study_version(session=session, study_version=body)
    return upd_study_version

@mod.post("/publish-study-version/{study_version_id}", status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def publish_study_version(
    study_version_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    await study_version_service.publish_study_version(session=session, study_version_id=study_version_id, request=request)

def init_app(app):
    app.include_router(mod, tags=["study-version"])
