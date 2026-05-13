from gearbox import config
from fastapi import APIRouter
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from gearbox.services import match_form as match_form_service, study as study_service
from . import logger
from starlette.responses import JSONResponse
from gearbox import auth
from gearboxdatamodel.schemas import MatchForm, MatchFormUpdate
from gearbox import deps
from gearboxdatamodel.util import status
from gearbox.util import bucket_utils
from gearbox.admin_login import admin_required, super_admin_required

mod = APIRouter()
bearer = HTTPBearer(auto_error=False)

@mod.post("/build-match-form/", response_model=MatchForm, response_model_exclude_none=True, dependencies=[ Depends(auth.authenticate), Depends(super_admin_required)] )
async def build_match_form(
    request: Request,
    session: Session = Depends(deps.get_session),
    save: bool = True
):
    """
    Comments: This endpoint is used to build the match form from the db. If the optional parameter 'save'
    is set to true, it will save the match for to S3, if 'save' is false it will just return
    the match form without uploading to S3. 
    """
    #update fe matching files and middleware cache after match form is updated
    await study_service.refresh_study_fe_files(session=session, request=request)
    return await match_form_service.build_match_form(session=session, request=request, save=save)


@mod.post("/update-match-form", dependencies=[ Depends(auth.authenticate), Depends(super_admin_required)])
async def update_match_form(
    body: MatchFormUpdate,
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
