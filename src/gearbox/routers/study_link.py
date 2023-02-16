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
from gearbox.schemas import StudyLinkSearchResults, StudyLink as StudyLinkSchema, StudyLinkCreate
from gearbox import deps
from gearbox.services import study_link  as study_link_service
from gearbox.admin_login import admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/study-link/{study_link_id}", response_model=StudyLinkSchema, dependencies=[Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_study_link(
    request: Request,
    study_link_id: int,
    session: AsyncSession = Depends(deps.get_session),
    token: HTTPAuthorizationCredentials = Security(bearer)
):
    ret_study_link = await study_link_service.get_single_study_link(session, study_link_id)
    return JSONResponse(jsonable_encoder(ret_study_link), status.HTTP_200_OK)

@mod.get("/study-links", response_model=StudyLinkSearchResults, dependencies=[Depends(auth.authenticate)])
async def get_all_study_links(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
    token: HTTPAuthorizationCredentials = Security(bearer)
):
    study_links = await study_link_service.get_study_links(session)
    return JSONResponse(jsonable_encoder(study_links), status.HTTP_200_OK)

@mod.post("/study-link", response_model=StudyLinkSchema,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: StudyLinkCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    new_study_link = await study_link_service.create_study_link(session, body)
    await session.commit()
    return JSONResponse(jsonable_encoder(new_study_link), status.HTTP_201_CREATED)

@mod.post("/update-study-link/{study_link_id}", response_model=StudyLinkSchema, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    study_link_id: int,
    body: dict,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    upd_study_link = await study_link_service.update_study_link(session=session, study_link=body, study_link_id=study_link_id)
    return JSONResponse(jsonable_encoder(upd_study_link), status.HTTP_201_CREATED)

def init_app(app):
    app.include_router(mod, tags=["study_link","update_study_link","study_links"])
