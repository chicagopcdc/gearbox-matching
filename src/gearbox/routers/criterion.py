from fastapi import Depends

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from authutils.token.fastapi import access_token
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from urllib.parse import urljoin
from pydantic import BaseModel
from fastapi import Request, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import logger
from gearbox.util import status
from gearbox.services import criterion
from starlette.responses import JSONResponse
from gearbox.admin_login import admin_required

# from gearbox import config
from gearbox.schemas import CriterionSearchResults, CriterionCreateIn, CriterionCreate, CriterionHasValueCreate, CriterionHasTagCreate, DisplayRulesCreate, TriggeredByCreate, Criterion
from gearbox.crud import criterion_crud, criterion_has_value_crud, criterion_has_tag_crud, display_rules_crud, triggered_by_crud, value_crud, tag_crud
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

# auto_error=False prevents FastAPI from raises a 403 when the request is missing
# an Authorization header. Instead, we want to return a 401 to signify that we did
# not recieve valid credentials
# bearer = HTTPBearer(auto_error=False)

@mod.get("/criteria", response_model=CriterionSearchResults, dependencies=[ Depends(auth.authenticate)])
async def get_criteria(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    criteria = await criterion_crud.get(session)
    return JSONResponse(jsonable_encoder(criteria), status.HTTP_200_OK)    

@mod.get("/criterion/{id}", response_model=Criterion, dependencies=[ Depends(auth.authenticate)])
async def get_criteria(
    request: Request,
    id: int,
    session: AsyncSession = Depends(deps.get_session),
):

    criterion = await criterion_crud.get(session, id=id)
    return JSONResponse(jsonable_encoder(criterion), status.HTTP_200_OK)    

@mod.post("/criterion", response_model=CriterionSearchResults,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: CriterionCreateIn,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    new_criterion = await criterion.create_new_criterion(session, body)
    await session.commit()
    return JSONResponse(new_criterion, status.HTTP_201_CREATED)

def init_app(app):
    app.include_router(mod, tags=["criteria","criterion"])