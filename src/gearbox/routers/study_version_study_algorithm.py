from fastapi import Depends

from collections.abc import Iterable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends
from . import logger
from gearbox.util import status
from gearbox.admin_login import admin_required

from gearbox.schemas import StudyVersionStudyAlgorithmCreate, StudyVersionStudyAlgorithm
from gearbox.services import study_version_study_algorithm as study_version_study_algorithm_service
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.post("/study-version-study-algorithm", response_model=StudyVersionStudyAlgorithm, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: StudyVersionStudyAlgorithmCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    new_svsa = await study_version_study_algorithm_service.create_study_version_study_algorithm(session=session, study_version_study_algorithm=body)
    return new_svsa

def init_app(app):
    app.include_router(mod, tags=["study-version-study-algorithm"])