from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends

from . import logger
from gearbox.util import status
from gearbox.services import raw_criteria as raw_criteria_service
from gearbox.admin_login import admin_required

from gearbox.schemas import RawCriteriaIn, RawCriteria
from gearbox.crud import raw_criteria_crud
from gearbox import deps
from gearbox import auth 
from starlette.responses import JSONResponse 

mod = APIRouter()

@mod.get("/raw-criteria/{raw_criteria_id}", response_model=RawCriteria, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_raw_criteria(
    raw_criteria_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    raw_criteria = await raw_criteria_service.get_raw_criteria(session=session, id=raw_criteria_id)
    return raw_criteria

@mod.get("/raw-criteria-ec/{eligibility_criteria_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate)])
async def get_criteria_by_eligibility_criteria_id(
    eligibility_criteria_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    """
    Comments: Get raw criteria (text only) by eligibility criteria id
    """
    raw_criteria = await raw_criteria_service.get_raw_criteria_by_eligibility_criteria_id(session, eligibility_criteria_id=eligibility_criteria_id)
    return raw_criteria


@mod.post("/raw-criteria", response_model=RawCriteria, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: RawCriteriaIn,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments: Save raw_criteria 
    """
    new_raw_criteria = await raw_criteria_service.create_raw_criteria(session, body)
    return JSONResponse(status.HTTP_200_OK)

def init_app(app):
    app.include_router(mod, tags=["raw-criteria"])