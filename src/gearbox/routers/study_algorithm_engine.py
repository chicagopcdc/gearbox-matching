from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter 
from fastapi import Request, Depends
from . import logger
from gearbox.util import status
from gearbox.admin_login import admin_required
from gearbox.services import study_algorithm_engine

from gearbox.schemas import StudyAlgorithmEngineUpdate, StudyAlgorithmEngineSearchResults , StudyAlgorithmEngine, StudyAlgorithmEngineCreateInput, StudyAlgorithmEngineCreate
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.get("/study-algorithm-engines", response_model=StudyAlgorithmEngineSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_saes(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    aes = await study_algorithm_engine.get_study_algorithm_engines(session=session)
    return { "results": list(aes) }

@mod.get("/study-algorithm-engine/{algorithm_engine_id}", response_model=StudyAlgorithmEngine, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_sae(
    algorithm_engine_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    sae = await study_algorithm_engine.get_study_algorithm_engine(session=session, id=algorithm_engine_id)
    return sae

@mod.post("/study-algorithm-engine", response_model=StudyAlgorithmEngine,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_sae(
    body: StudyAlgorithmEngineCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments: This endpoint installs the logic for a partiular study version into the db.
    """
    print(f"IN POST----------------------")
    print(f"HERE IN ROUTER BODY: {body}")
    new_ae = await study_algorithm_engine.create(session=session, study_algorithm_engine=body.study_algorithm_engine, eligibility_criteria_info_id=body.eligibility_criteria_info_id)
    print(f"TYPE NEW AE: --------- {type(new_ae)}")
    print(f"NEW AE: {new_ae.id}")
    print(f"NEW AE: {new_ae.start_date}")
    print(f"NEW AE: {new_ae.algorithm_version}")
    print(f"NEW AE: {new_ae.algorithm_logic}")
    return new_ae

@mod.post("/update-study-algorithm-engine", response_model=StudyAlgorithmEngine,dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def update_sae(
    body: StudyAlgorithmEngineUpdate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments: This endpoint updates the logic for a partiular study version 
    """
    updated_sae = await study_algorithm_engine.update(session=session, study_algorithm_engine=body)
    return updated_sae

def init_app(app):
    app.include_router(mod, tags=["study-algorithm-engine"])
