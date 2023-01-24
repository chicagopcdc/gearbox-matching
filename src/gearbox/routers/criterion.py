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
from starlette.responses import JSONResponse
from gearbox.admin_login import admin_required

# from gearbox import config
from gearbox.schemas import CriterionSearchResults, CriterionCreateIn, CriterionCreate, CriterionHasValueCreate, CriterionHasTagCreate, DisplayRulesCreate, TriggeredByCreate
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

@mod.post("/criterion", response_model=CriterionSearchResults,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: CriterionCreateIn,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    body_conv = jsonable_encoder(body)

    # check input fks exist
    check_id_errors = []

    # triggered_by_value_id and triggered_by_criterion_id must both be populated or both null
    if not (body.triggered_by_value_id == None) == (body.triggered_by_criterion_id == None):
        check_id_errors.append('Input data must include both or neither triggered_by_value_id and triggered_by_criterion_id')
    elif body.triggered_by_value_id:
        check_id_errors.append(await value_crud.check_key(db=session, ids_to_check=body.triggered_by_value_id))
        check_id_errors.append(await criterion_crud.check_key(db=session, ids_to_check=body.triggered_by_criterion_id))

    check_id_errors.append(await value_crud.check_key(db=session, ids_to_check=body.values))
    check_id_errors.append(await tag_crud.check_key(db=session, ids_to_check=body.tags))
    check_id_errors.append(await tag_crud.check_key(db=session, ids_to_check=body.tags))

    if not all(i is None for i in check_id_errors):
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"ERROR: missing FKs for criterion creation: {[error for error in check_id_errors if error]}")        

    # Build CriterionCreate object from input - exclude triggered_by, display_rules, tags, and values
    # which are separate inserts
    criterion_create = { key:value for key,value in body_conv.items() if key in CriterionCreate.__fields__.keys() }
    new_criterion = await criterion_crud.create(db=session, obj_in=criterion_create)

    if body.values:
        for v_id in body.values:
            chv = CriterionHasValueCreate(criterion_id=new_criterion.id, value_id=v_id)
            new_value = await criterion_has_value_crud.create(db=session,obj_in=chv)

    # if it is determined that tags are not required, check if exists here before create 
    for t_id in body.tags:
        thv = CriterionHasTagCreate(criterion_id=new_criterion.id, tag_id=t_id)
        new_value = await criterion_has_tag_crud.create(db=session,obj_in=thv)

    dr = DisplayRulesCreate(criterion_id=new_criterion.id, 
        priority=body.display_rules_priority,
        version=body.display_rules_version
        )
    new_display_rule = await display_rules_crud.create(db=session, obj_in=dr)

    if body.triggered_by_criterion_id:
        tb = TriggeredByCreate(display_rules_id=new_display_rule.id,
            criterion_id=body.triggered_by_criterion_id,
            value_id=body.triggered_by_value_id,
            path=body.triggered_by_path
        )
        new_triggered_by = await triggered_by_crud.create(db=session, obj_in=tb)

    return JSONResponse(jsonable_encoder(new_criterion), status.HTTP_201_CREATED)

def init_app(app):
    app.include_router(mod, tags=["criteria","criterion"])