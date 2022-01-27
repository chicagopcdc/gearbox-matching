from fastapi import APIRouter
import json
from sqlalchemy.orm import Session, joinedload
# from sqlalchemy import func, update, select, exc 
from fastapi import Request, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from typing import List

from .. import config, logger, auth
from ..models.models import Site, SiteHasStudy
from ..schemas import SiteSchema
# from ..crud.site import get_all_sites, get_singsite
from ..crud.site import get_single_site, get_sites
from .. import deps

mod = APIRouter()

@mod.get("/site/{site_id}", response_model=List[SiteSchema], status_code=HTTP_200_OK)
async def get_site(
    request: Request,
    site_id: int,
    session: Session = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    auth_header = str(request.headers.get("Authorization", ""))
    results = await get_single_site(session, site_id)
    return results

@mod.get("/sites", response_model=List[SiteSchema], status_code=HTTP_200_OK)
async def get_all_sites(
    request: Request,
    session: Session = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    auth_header = str(request.headers.get("Authorization", ""))
    results = await get_sites(session)
    return results

def init_app(app):
    app.include_router(mod, tags=["site"])