from fastapi import Depends

from collections.abc import Iterable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends
from . import logger
from gearbox.util import status
from gearbox.admin_login import admin_required

from gearbox.schemas import ValueCreate, ValueSearchResults, Value
from gearbox.services import value as value_service
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.get("/values", response_model=ValueSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_values(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    values = await value_service.get_values(session=session)
    return { "results" :list(values) }

@mod.get("/value/{value_id}", response_model=Value, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_value(
    value_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    ret_value = await value_service.get_value(session=session, id=value_id)
    return ret_value

@mod.post("/value", response_model=Value, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: ValueCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    new_value = await value_service.create_value(session=session, value=body)
    return new_value

@mod.post("/update-value/{value_id}", response_model=Value, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_object(
    value_id: int,
    body: dict,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    upd_value = await value_service.update_value(session=session, value=body, value_id=value_id)
    return upd_value

def init_app(app):
    app.include_router(mod, tags=["value","values","update-value"])
