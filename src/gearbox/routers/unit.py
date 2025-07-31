from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends, APIRouter, HTTPException
from . import logger
from ..util import status
from gearbox import auth
from gearbox.schemas import UnitSearchResults, Unit as UnitSchema, UnitCreate
from gearbox import deps
from gearbox.services import unit  as unit_service
from gearbox.admin_login import admin_required

mod = APIRouter()

@mod.get("/unit/{unit_id}", response_model=UnitSchema, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate), Depends(admin_required)] )
async def get_unit(
    request: Request,
    unit_id: int,
    session: AsyncSession = Depends(deps.get_session)
):
    unit = await unit_service.get_single_unit(session, unit_id)
    if not unit:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
            f"unit not found for id: {unit_id}")
    else:
        return unit

@mod.get("/units", response_model=UnitSearchResults, status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate), Depends(admin_required)])
async def get_all_units(
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    units = await unit_service.get_units(session)
    return { "results": list(units)}

@mod.post("/unit", response_model=UnitSchema,status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_unit(
    body: UnitCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    new_unit = await unit_service.create_unit(session=session, unit=body)
    await session.commit()
    return new_unit

@mod.post("/update-unit/{unit_id}", status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_unit(
    unit_id: int,
    body: dict,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    await unit_service.update_unit(session=session, unit=body, unit_id=unit_id)

def init_app(app):
    app.include_router(mod, tags=["unit"])
