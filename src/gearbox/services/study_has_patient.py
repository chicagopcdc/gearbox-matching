from . import logger
from gearboxdatamodel.crud import study_has_patient_crud
from gearboxdatamodel.schemas import StudyHasPatientCreate, StudyHasPatientSearchResults
from gearboxdatamodel.schemas import StudyHasPatient as StudyHasPatientSchema
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select
from fastapi import HTTPException
from gearboxdatamodel.util import status
from gearboxdatamodel.models import StudyHasPatient
from gearboxdatamodel.crud import study_has_patient
from typing import List
from pydantic import ValidationError

async def get_study_has_patients(session: Session, column: str, id: str) -> StudyHasPatientSearchResults:

    results = await study_has_patient_crud.get_multi(db=session, where=[f"study_has_patient.{column} = {id}"])
    return results


async def create_study_has_patient(session: Session, study_has_patient: List[StudyHasPatientSchema]) -> StudyHasPatientSearchResults:
    shps = []
    for shp in study_has_patient:
        try:
            StudyHasPatientSchema(**shp)
            new_study_has_patient = await study_has_patient_crud.create(db=session, obj_in=shp)
            shps.append(new_study_has_patient)
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'{e}')
    await session.commit()
    return shps