from . import logger
from gearbox.crud import study_has_patient_crud
from gearbox.schemas import StudyHasPatientCreate, StudyHasPatientSearchResults, StudyHasPatientSchema
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select
from fastapi import HTTPException
from gearbox.util import status
from gearbox.models import study_has_patient as study_has_patient_model

# create getters to retrieve all patients for a given study, all studies for a given patient, and all study_has_patient records
# for a given study and/or patient
async def get_study_has_patients(session: Session, id: int = None) -> StudyHasPatientSearchResults:
    if id:
        stmt = select(study_has_patient_model).where(study_has_patient_model.study_id == id)
    else:
        stmt = select(study_has_patient_model)
    results = await session.execute(stmt)
    study_has_patients = results.scalars().all()
    return study_has_patients

async def get_patient_has_studies(session: Session, id: int = None) -> StudyHasPatientSearchResults:
    if id:
        stmt = select(study_has_patient_model).where(study_has_patient_model.patient_id == id)
    else:
        stmt = select(study_has_patient_model)
    results = await session.execute(stmt)
    patient_has_studies = results.scalars().all()
    return patient_has_studies

# create set method to add a study patient entry to our table:
# given a study_has_patient object, create a new study_has_patient record in the database
async def create_study_has_patient(session: Session, study_has_patient: StudyHasPatientCreate) -> StudyHasPatientSearchResults:
    shps = []
    for shp in study_has_patient.shps:
        new_study_has_patient = await study_has_patient_crud.create(db=session, obj_in=shp)
        shps.append(new_study_has_patient)
    await session.commit() 
    return shps