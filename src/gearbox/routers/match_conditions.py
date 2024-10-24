from re import I
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Security
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi import Request, Depends 
from gearbox import config
from starlette.responses import JSONResponse
from typing import List
from gearbox import auth
from gearbox.schemas import AlgorithmResponse
from gearbox import deps
from gearbox.services import match_conditions as mc
from gearbox.util import status, bucket_utils
from gearbox.admin_login import admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.get("/match-conditions", dependencies=[ Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_mc(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    """
    Comments: This endpoint is called by the front-end to return the presigned_url to the S3
    bucket that contains the match conditions file
    """
    params = []
    presigned_url = bucket_utils.get_presigned_url(request, config.S3_BUCKET_MATCH_CONDITIONS_KEY_NAME, params, "get_object")
    return JSONResponse(presigned_url, status.HTTP_200_OK)

@mod.post("/build-match-conditions", response_model=List[AlgorithmResponse], dependencies=[ Depends(auth.authenticate), Depends(admin_required)], status_code=status.HTTP_200_OK)
async def build_mc(
    request: Request,
    session: Session = Depends(deps.get_session)
):

    match_conditions = await mc.get_match_conditions(session)

    if not config.BYPASS_S3:
        params = [{'Content-Type':'application/json'}]
        bucket_utils.put_object(request, config.S3_BUCKET_NAME, config.S3_BUCKET_MATCH_CONDITIONS_KEY_NAME, config.S3_PUT_OBJECT_EXPIRES, params, match_conditions)
    return JSONResponse(jsonable_encoder(match_conditions), status.HTTP_200_OK)

def init_app(app):
    app.include_router(mod, tags=["match-conditions"])
