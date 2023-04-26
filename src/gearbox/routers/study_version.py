from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends
from fastapi import APIRouter 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import date
from . import logger
from ..util import status
from gearbox import auth
from gearbox.schemas import StudyVersionSearchResults, StudyVersion as StudyVersionSchema, StudyVersionCreate
from gearbox import deps
from gearbox.services import study_version  as study_version_service
from gearbox.admin_login import admin_required

mod = APIRouter()

@mod.get("/study-version/{study_version_id}", response_model=StudyVersionSchema, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate)] )
async def get_study_version(
    request: Request,
    study_version_id: int,
    session: AsyncSession = Depends(deps.get_session),
):
    ret_study_version = await study_version_service.get_study_version(session, study_version_id)
    return ret_study_version

@mod.get("/study-versions", response_model=StudyVersionSearchResults, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate)])
async def get_all_study_versions(
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    study_versions = await study_version_service.get_study_versions(session)
    return {"results": list(study_versions)}

@mod.post("/study-version", response_model=StudyVersionSchema, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: StudyVersionCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    new_study_version = await study_version_service.create_study_version(session, body)
    await session.commit()
    return new_study_version

"""
@mod.post("/study-version", response_model=StudyVersionSchema,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: StudyVersionCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    new_study_version = await study_version_service.create_study_version(session, body)
    await session.commit()
    return JSONResponse(jsonable_encoder(new_study_version), status.HTTP_201_CREATED)
"""

@mod.post("/update-study-version/{study_version_id}", response_model=StudyVersionSchema, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    study_version_id: int,
    body: dict,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    upd_study_version = await study_version_service.update_study_version(session=session, study_version=body, study_version_id=study_version_id)
    return upd_study_version

def init_app(app):
    app.include_router(mod, tags=["study_version","update_study_version","study_versions"])
