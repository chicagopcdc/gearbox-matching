import os
import datetime
import httpx
import fastapi
from fastapi import Depends
import jwt

from collections.abc import Iterable
from enum import Enum
from typing import List
from asyncpg import UniqueViolationError
from sqlalchemy.ext.asyncio.session import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from authutils.token.fastapi import access_token
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from urllib.parse import urljoin
from pydantic import BaseModel
from fastapi import Request, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from gearbox.models import display_rules
from . import logger
from ..util import status
from starlette.responses import JSONResponse
from ..admin_login import admin_required

from .. import config
from ..schemas import CriterionSearchResults, CriterionCreateIn, CriterionCreate, CriterionHasValueCreate, CriterionHasTagCreate, DisplayRulesCreate, TriggeredByCreate
from ..crud import criterion, criterion_has_value, criterion_has_tag, display_rules_crud, triggered_by_crud, value, tag
from .. import deps
from .. import auth 

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

    auth_header = str(request.headers.get("Authorization",""))
    criteria = await criterion.get_multi(session)
    return JSONResponse(jsonable_encoder(criteria), status.HTTP_200_OK)    

@mod.post("/criterion", response_model=CriterionSearchResults,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: CriterionCreateIn,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    auth_header = str(request.headers.get("Authorization",""))
    logger.info(f"-----------------------------> HERE???")
    # CREATE ORM OBJECTS FROM tag, value ids - do queries to get vals?
    body_conv = jsonable_encoder(body)
    # TO DO: validate incoming value_ids and tag_ids to make sure they already
    # exist, if not then throw an exception - do this before creating the 
    # criteria and all associated rows in other tables

    # CREATE A FUNCTION FOR THE FOLLOWING CHECKS AND PUT IN util
    check_id_errors = await value.check_key(db=session, ids_to_check=body.values)
    if check_id_errors:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR: creating criterion: {check_id_errors}")        

    check_id_errors = await value.check_key(db=session, ids_to_check=body.triggered_by_value_id)
    if check_id_errors:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR: creating criterion triggered_by: {check_id_errors}")        

    check_id_errors = await tag.check_key(db=session, ids_to_check=body.tags)
    if check_id_errors:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR: creating criterion tag: {check_id_errors}")        

    # Build CriterionCreate object from input
    criterion_create = { key:value for key,value in body_conv.items() if key in CriterionCreate.__fields__.keys() }
    new_criterion = await criterion.create(db=session, obj_in=criterion_create)
  
    for v_id in body.values:
        chv = CriterionHasValueCreate(criterion_id=new_criterion.id, value_id=v_id)
        new_value = await criterion_has_value.create(db=session,obj_in=chv)
    
    for t_id in body.tags:
        thv = CriterionHasTagCreate(criterion_id=new_criterion.id, tag_id=t_id)
        new_value = await criterion_has_tag.create(db=session,obj_in=thv)

    dr = DisplayRulesCreate(criterion_id=new_criterion.id, 
        priority=body.display_rules_priority,
        version=body.display_rules_version
        )
    new_display_rule = await display_rules_crud.create(db=session, obj_in=dr)

    tb = TriggeredByCreate(display_rules_id=new_display_rule.id,
        criterion_id=new_criterion.id,
        value_id=body.triggered_by_value_id,
        path=body.triggered_by_path
    )
    new_triggered_by = await triggered_by_crud.create(db=session, obj_in=tb)
    """
   display_rules_id: int
    criterion_id: int
    value_id: int
    path: Optional[str]

    display_rules_priority: int
    display_rules_version: Optional[int]
    triggered_by_value_id: Optional[int]
    triggered_by_path: Optional[str]
    """

    return JSONResponse(jsonable_encoder(new_criterion), status.HTTP_201_CREATED)

#    Comments:
#    auth_header = str(request.headers.get("Authorization",""))
#    value = await add_value(session, body)
#    return JSONResponse(jsonable_encoder(value), status.HTTP_201_CREATED)

def init_app(app):
    app.include_router(mod, tags=["criteria","criterion"])
