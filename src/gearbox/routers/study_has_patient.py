from fastapi import Depends

from collections.abc import Iterable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, APIRouter
from fastapi import Request, Depends
from . import logger
from gearbox.util import status
from gearbox.admin_login import admin_required

from gearbox.schemas import study_has_patientCreate, study_has_patientSearchResults, study_has_patient, study_has_patients
from gearbox.services import study_has_patient as study_has_patient_service
from gearbox import deps
from gearbox import auth 
from gearbox import config

mod = APIRouter()

# create methods to get all patients for a study, get all studies for a patient, and add a patient to a study
@mod.get("/study-has-patients", response_model=study_has_patientSearchResults, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_study_has_patients(
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    if not config.STUDY_HAS_PATIENT:
        raise HTTPException(status_code=404, detail="Study Has Patient endpoints are not enabled")
    
    study_has_patients = await study_has_patient_service.get_study_has_patients(session=session)
    return { "results" :list(study_has_patients) }

@mod.get("/study-has-patients/{study_id}", response_model=study_has_patient, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_study_has_patients(
    study_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    if not config.STUDY_HAS_PATIENT:
        raise HTTPException(status_code=404, detail="Study Has Patient endpoints are not enabled")
    
    ret_study_has_patients = await study_has_patient_service.get_study_has_patients(session=session, id=study_id)
    return ret_study_has_patients

@mod.get("/patient-has-studies/{patient_id}", response_model=study_has_patient, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate)])
async def get_patient_has_studies(
    patient_id: int,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    if not config.STUDY_HAS_PATIENT:
        raise HTTPException(status_code=404, detail="Study Has Patient endpoints are not enabled")
    
    ret_patient_has_studies = await study_has_patient_service.get_patient_has_studies(session=session, id=patient_id)
    return ret_patient_has_studies

@mod.post("/study-has-patient", response_model=study_has_patients, status_code=status.HTTP_200_OK, dependencies=[ Depends(auth.authenticate), Depends(admin_required)])
async def save_object(
    body: study_has_patientCreate,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    if not config.STUDY_HAS_PATIENT:
        raise HTTPException(status_code=404, detail="Study Has Patient endpoints are not enabled")
    
    new_study_has_patient = await study_has_patient_service.create_study_has_patient(session=session, study_has_patient=body)
    return { "shps" :list(new_study_has_patient) }

def init_app(app):
    app.include_router(mod, tags=["study-has-patient","update_study_has_patient","study_has_patients"])
