from .base import CRUDBase
from gearbox.models import StudyHasPatient
from gearbox.schemas import StudyHasPatientCreate, StudyHasPatientSearchResults

class CRUDStudyHasPatient(CRUDBase [StudyHasPatient, StudyHasPatientCreate, StudyHasPatientSearchResults]):
    ...
study_has_patient_crud = CRUDStudyHasPatient(StudyHasPatient)