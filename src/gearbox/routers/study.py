import json
from fastapi import APIRouter
from sqlalchemy.orm import Session
from datetime import date
from time import gmtime, strftime
from fastapi import Request, Depends
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
from .. import logger, auth
from ..schemas import StudySchema, StudyResponse
from ..crud.study import get_single_study, get_studies
from .. import deps

mod = APIRouter()

@mod.get("/study/{study_id}", response_model=StudyResponse, status_code=HTTP_200_OK)
async def get_study(
    request: Request,
    study_id: int,
    session: Session = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    auth_header = str(request.headers.get("Authorization", ""))
    results = await get_single_study(session, study_id)

    response = {
                "current_date": date.today().strftime("%B %d, %Y"),
                "current_time": strftime("%H:%M:%S +0000", gmtime()),
                "status": "OK",
                "body": results
    }

    return response

@mod.get("/studies", response_model=StudyResponse, status_code=HTTP_200_OK)
async def get_all_studies(
    request: Request,
    session: Session = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    auth_header = str(request.headers.get("Authorization", ""))
    results = await get_studies(session)
    response = {
                "current_date": date.today().strftime("%B %d, %Y"),
                "current_time": strftime("%H:%M:%S +0000", gmtime()),
                "status": "OK",
                "body": results
    }

    return response

def init_app(app):
    app.include_router(mod, tags=["study"])