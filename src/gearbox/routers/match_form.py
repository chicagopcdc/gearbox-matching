from gearbox import config
from fastapi import APIRouter
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from gearbox.services import match_form as match_form_service
from . import logger
from starlette.responses import JSONResponse
from gearbox import auth
from gearbox.schemas import MatchForm
from gearbox.schemas.match_form import showif_logic_schema
from gearbox import deps
from gearbox.util import status, bucket_utils
from gearbox.admin_login import admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.post("/build-match-form/", response_model=MatchForm, response_model_exclude_none=True, dependencies=[ Depends(auth.authenticate), Depends(admin_required)] )
async def build_match_info(
    request: Request,
    session: Session = Depends(deps.get_session),
    save: bool = True
):
    """
    Comments: This endpoint is used to build the match form from the db. If the optional parameter 'save'
    is set to true, it will save the match for to S3, if 'save' is false it will just return
    the match form without uploading to S3. 
    """
    print(f"-----------> MATCH FORM INFO: {showif_logic_schema}")

    match_form = await match_form_service.get_match_form(session)
    if save:
        if not config.BYPASS_S3:
            params = [{'Content-Type':'application/json'}]
            bucket_utils.put_object(request, config.S3_BUCKET_NAME, config.S3_BUCKET_MATCH_FORM_KEY_NAME, config.S3_PUT_OBJECT_EXPIRES, params, match_form)

    return match_form

@mod.get("/match-form", dependencies=[ Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_match_form(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    params = []
    presigned_url = bucket_utils.get_presigned_url(request, config.S3_BUCKET_MATCH_FORM_KEY_NAME, params, "get_object")
    return JSONResponse(presigned_url, status.HTTP_200_OK)

@mod.get("/important-questions", dependencies=[ Depends(auth.authenticate)], status_code=status.HTTP_200_OK)
async def get_match_form(
    request: Request,
    session: Session = Depends(deps.get_session)
):
    params = []
    presigned_url = bucket_utils.get_presigned_url(request, config.S3_BUCKET_IMPORTANT_QUESTIONS_KEY_NAME, params, "get_object")
    return JSONResponse(presigned_url, status.HTTP_200_OK)

@mod.post("/update-match-form", dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_sae(
    body: MatchForm,
    request: Request,
    session: Session = Depends(deps.get_session),
):
    """
    Comments: This endpoint is used to update the order of the criteria in the match_form.
    It deletes and recreates the contents of the display_rules and triggered_by tables based
    on the given match form json.
    """
    await match_form_service.update(match_form=body, session=session)
    return JSONResponse(status.HTTP_200_OK)

def init_app(app):
    app.include_router(mod, tags=["match-form"])
