from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends

from . import logger
from gearbox.util import status
from gearbox.services import criterion as criterion_service
from gearbox.admin_login import admin_required

from gearbox.schemas import DisplayRulesSearchResults
from gearbox.crud import display_rules_crud
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.get("/display-rules", response_model=DisplayRulesSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_criteria(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    display_rules = await display_rules_crud.get_multi(session)
    return { "results" :list(display_rules) }

def init_app(app):
    app.include_router(mod, tags=["display-rules"])