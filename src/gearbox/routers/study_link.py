from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends, APIRouter, HTTPException
from . import logger
from gearboxdatamodel.util import status
from gearbox import auth
from gearboxdatamodel.schemas import StudyLinkSearchResults, StudyLink as StudyLinkSchema, StudyLinkCreate
from gearbox import deps
from gearbox.services import study_link  as study_link_service
from gearbox.admin_login import admin_required

mod = APIRouter()

@mod.get("/study-link/{study_link_id}", response_model=StudyLinkSchema, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate), Depends(admin_required)] )
async def get_study_link(
    request: Request,
    study_link_id: int,
    session: AsyncSession = Depends(deps.get_session)
):
    ret_study_link = await study_link_service.get_single_study_link(session, study_link_id)
    if not ret_study_link:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
            f"study link not found for id: {study_link_id}")
    else:
        return ret_study_link
    return ret_study_link

@mod.get("/study-links", response_model=StudyLinkSearchResults, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate), Depends(admin_required)])
async def get_all_study_links(
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    study_links = await study_link_service.get_study_links(session)
    return { "results": list(study_links)}

@mod.post("/study-link", response_model=StudyLinkSchema,status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: StudyLinkCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    new_study_link = await study_link_service.create_study_link(session=session, study_link=body)
    await session.commit()
    return new_study_link

@mod.post("/update-study-link/{study_link_id}", status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    study_link_id: int,
    body: dict,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    await study_link_service.update_study_link(session=session, study_link=body, study_link_id=study_link_id)

def init_app(app):
    app.include_router(mod, tags=["study-link"])
