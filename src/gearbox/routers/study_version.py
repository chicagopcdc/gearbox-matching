from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import date
from time import gmtime, strftime
from . import logger
from ..util import status
from starlette.responses import JSONResponse
from typing import List
from gearbox import auth
from gearbox.schemas import StudyVersionSearchResults, StudyVersion as StudyVersionSchema, StudyVersionCreate
from gearbox import deps
from gearbox.services import study_version  as study_version_service
from gearbox.admin_login import admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/study-version/{study_version_id}", response_model=StudyVersionSchema, dependencies=[Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_study_version(
    request: Request,
    study_version_id: int,
    session: AsyncSession = Depends(deps.get_session),
    token: HTTPAuthorizationCredentials = Security(bearer)
):
    ret_study_version = await study_version_service.get_single_study_version(session, study_version_id)
    return JSONResponse(jsonable_encoder(ret_study_version), status.HTTP_200_OK)

@mod.get("/study-versions", response_model=StudyVersionSearchResults, dependencies=[Depends(auth.authenticate)])
async def get_all_study_versions(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    token: HTTPAuthorizationCredentials = Security(bearer)
):
    study_versions = await study_version_service.get_study_versions(session)
    return JSONResponse(jsonable_encoder(study_versions), status.HTTP_200_OK)

@mod.post("/study-version", response_model=StudyVersionSchema,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: StudyVersionCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    new_study_version = await study_version_service.create_study_version(session, body)
    await session.commit()
    return JSONResponse(jsonable_encoder(new_study_version), status.HTTP_201_CREATED)

@mod.post("/update-study-version/{study_version_id}", response_model=StudyVersionSchema, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
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
    return JSONResponse(jsonable_encoder(upd_study_version), status.HTTP_201_CREATED)

def init_app(app):
    app.include_router(mod, tags=["study_version","update_study_version","study_versions"])
