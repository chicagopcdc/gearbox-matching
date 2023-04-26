from .base import CRUDBase
from gearbox.models import StudyVersion
from gearbox.schemas import StudyVersionSearchResults, StudyVersionCreate

class CRUDStudyVersion(CRUDBase [StudyVersion, StudyVersionCreate, StudyVersionSearchResults]):
    ...
study_version_crud = CRUDStudyVersion(StudyVersion)
