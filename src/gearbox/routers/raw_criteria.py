from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request, Depends, UploadFile, File, HTTPException
import io, fnmatch, json

from . import logger
from gearboxdatamodel.util import status
from gearbox.services import raw_criteria as raw_criteria_service
from gearbox.admin_login import admin_required

from gearboxdatamodel.schemas import RawCriteriaIn, RawCriteria
from gearbox import deps
from gearbox import auth 
from starlette.responses import JSONResponse 
import zipfile

mod = APIRouter()

@mod.get("/raw-criteria/{raw_criteria_id}", response_model=RawCriteria, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def get_raw_criteria(
    raw_criteria_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):

    raw_criteria = await raw_criteria_service.get_raw_criteria(session=session, id=raw_criteria_id)

    if not raw_criteria:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"raw-criterion not found for id: {raw_criteria_id}")
    return raw_criteria

@mod.get("/raw-criteria-ec/{eligibility_criteria_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth.authenticate), Depends(admin_required)])
async def get_criteria_by_eligibility_criteria_id(
    eligibility_criteria_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session)
):
    """
    Comments: Get raw criteria (text only) by eligibility criteria id
    """
    raw_criteria = await raw_criteria_service.get_raw_criteria_by_eligibility_criteria_id(session, eligibility_criteria_id=eligibility_criteria_id)
    if not raw_criteria:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
            f"raw_criteria not found for eligibility_criteria_id: {eligibility_criteria_id}")
    else:
        return raw_criteria


@mod.post("/raw-criteria", status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(file: UploadFile = File(...),
    session: AsyncSession = Depends(deps.get_session),
    user_id: int = Depends(auth.authenticate_user)
):
    """
    Comments: Save raw_criteria 
    """

    with zipfile.ZipFile(io.BytesIO(await file.read()),'r') as zip_ref:
        namelist = zip_ref.namelist()
        for filename in namelist:
            if fnmatch.fnmatch(filename, '*.jsonl'):
                # Create raw_criteria for all jsonl files in zipfile from doccano
                with zip_ref.open(filename) as file:
                    try:
                        contents = file.read()
                    except Exception as e:
                        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error reading file: {filename} error: {e}.")
                    await raw_criteria_service.create_raw_criteria(session, raw_criteria_str=contents, user_id=user_id)


    return JSONResponse(status.HTTP_200_OK)

def init_app(app):
    app.include_router(mod, tags=["raw-criteria"])
