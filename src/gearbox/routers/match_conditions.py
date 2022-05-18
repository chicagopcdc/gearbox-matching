import json
from re import I
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import date
from time import gmtime, strftime
from sqlalchemy.orm import Session
from fastapi import Request, Depends, HTTPException
from starlette.responses import JSONResponse
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
from .. import auth
from ..schemas import AlgorithmEngine, AlgorithmResponse, StudyResponse
from ..crud.match_conditions import get_match_conditions
from .. import deps
from ..util import match_conditions as mc
from ..admin_login import admin_required

import logging
logger = logging.getLogger('gb-logger')

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/match-conditions", response_model=List[AlgorithmResponse], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=HTTP_200_OK)
async def get_mc(
    request: Request,
    session: Session = Depends(deps.get_session)
):

    all_algo_engs = await get_match_conditions(session)
    response = []
    ae_dict = {}

    for ae in all_algo_engs:
        if ae.study_algo_engine.study_version.study_id in ae_dict:
                ae_dict[ae.study_algo_engine.study_version.study_id].append((ae.path,ae.sequence))
        else:
            ae_dict[ae.study_algo_engine.study_version.study_id] = [(ae.path,ae.sequence)]

    for i in sorted(ae_dict):
        study_id = i
        paths = [ x[0] for x in sorted(ae_dict[i], key = lambda x: x[1])]
        response.append(mc.get_tree(study_id, paths))

    return JSONResponse(response, HTTP_200_OK)

def init_app(app):
    app.include_router(mod, tags=["match_conditions"])
