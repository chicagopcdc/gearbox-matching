from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends

from gearbox.util import status
from gearbox.services import input_type as input_type_service

from gearbox.schemas import InputTypeSearchResults
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.get("/input-types", response_model=InputTypeSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_input_types(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    input_types = await input_type_service.get_input_types(session)
    return { "results" :list(input_types) }

def init_app(app):
    app.include_router(mod, tags=["input-type"])