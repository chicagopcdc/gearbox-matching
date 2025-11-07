from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends

from gearboxdatamodel.util import status
from gearbox.services import input_type as input_type_service

from gearboxdatamodel.schemas import InputTypeSearchResults
from gearbox import deps
from gearbox import auth 
from gearbox.admin_login import admin_required

mod = APIRouter()

@mod.get("/input-types", response_model=InputTypeSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def get_input_types(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    input_types = await input_type_service.get_input_types(session)
    return { "results" :list(input_types) }

def init_app(app):
    app.include_router(mod, tags=["input-type"])