from fastapi import Depends

from sqlalchemy.ext.asyncio.session import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from authutils.token.fastapi import access_token
from fastapi import APIRouter, Security
from fastapi import Request, Depends
from fastapi.encoders import jsonable_encoder
from . import logger
from gearbox.util import status
from starlette.responses import JSONResponse
from gearbox.admin_login import admin_required
from gearbox.services import study_algorithm_engine

from gearbox.schemas import StudyAlgorithmEngineCreate, StudyAlgorithmEngineSearchResults 
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.get("/study-algorithm-engines", response_model=StudyAlgorithmEngineSearchResults, dependencies=[ Depends(auth.authenticate)])
async def get_saes(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    aes = await study_algorithm_engine.get_study_algorithm_engines(session=session)
    return JSONResponse(jsonable_encoder(aes), status.HTTP_200_OK)

@mod.get("/study-algorithm-engine/{algorithm_engine_id}", response_model=StudyAlgorithmEngineSearchResults, dependencies=[ Depends(auth.authenticate)])
async def get_sae(
    algorithm_engine_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    sae = await study_algorithm_engine.get_study_algorithm_engine(session=session, id=algorithm_engine_id)
    return JSONResponse(jsonable_encoder(sae), status.HTTP_200_OK)

@mod.post("/study-algorithm-engine", response_model=StudyAlgorithmEngineSearchResults,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_sae(
    body: StudyAlgorithmEngineCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    new_ae = await study_algorithm_engine.create(session=session, study_algorithm_engine=body)
    return JSONResponse(jsonable_encoder(new_ae), status.HTTP_201_CREATED)

def init_app(app):
    app.include_router(mod, tags=["study-algorithm-engine","study-algorithm-engines"])