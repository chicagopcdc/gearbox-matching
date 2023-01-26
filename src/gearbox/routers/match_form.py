import json
from gearbox import config
import re
from datetime import date
from time import gmtime, strftime
from fastapi import APIRouter
from fastapi import APIRouter, Security
from sqlalchemy.orm import Session
from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer

from gearbox.services import match_conditions as mc, match_form as mf
from . import logger
from starlette.responses import JSONResponse 
from typing import List
from gearbox import auth
from gearbox.schemas import DisplayRules 
from gearbox.crud.match_form import get_form_info
from gearbox import deps
from gearbox.util.bounds import bounds
from gearbox.util import status, bucket_utils
from gearbox.admin_login import admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.post("/build-match-form", response_model=List[DisplayRules], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=status.HTTP_200_OK)
async def build_match_info(
    request: Request,
    session: Session = Depends(deps.get_session),
):
    match_form = await mf.get_match_form(session)

    if not config.BYPASS_S3:
        params = [{'Content-Type':'application/json'}]
        bucket_utils.put_object(request, config.S3_BUCKET_NAME, config.S3_BUCKET_MATCH_FORM_KEY_NAME, config.S3_PUT_OBJECT_EXPIRES, params, match_form)
    return JSONResponse(match_form, status.HTTP_200_OK)

@mod.get("/match-form", dependencies=[ Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_match_form(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    params = []
    presigned_url = bucket_utils.get_presigned_url(request, config.S3_BUCKET_MATCH_FORM_KEY_NAME, params, "get_object")
    return JSONResponse(presigned_url, status.HTTP_200_OK) 

def init_app(app):
    app.include_router(mod, tags=["build_match_form"])
    app.include_router(mod, tags=["match_form"])
