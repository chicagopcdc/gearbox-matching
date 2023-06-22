from fastapi import Depends

from collections.abc import Iterable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request, Depends
from . import logger
from gearbox.util import status
from gearbox.admin_login import admin_required

from gearbox.schemas import StudyVersionEligibilityCriteriaCreate, StudyVersionEligibilityCriteria
from gearbox.services import study_version_eligibility_criteria as study_version_eligibility_criteria_service
from gearbox import deps
from gearbox import auth 

mod = APIRouter()

@mod.post("/study-version-eligibility-criteria", response_model=StudyVersionEligibilityCriteria, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: StudyVersionEligibilityCriteriaCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """
    Comments:
    """
    new_svec = await study_version_eligibility_criteria_service.create_study_version_eligibility_criteria(session=session, study_version_eligibility_criteria=body)
    return new_svec

def init_app(app):
    app.include_router(mod, tags=["study-version-eligibility-criteria"])
