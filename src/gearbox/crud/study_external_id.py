from .base import CRUDBase
from gearbox.models import StudyExternalId
from gearbox.schemas import StudyExternalIdCreate, StudyExternalIdSearchResults

class CRUDStudyExternalId(CRUDBase [StudyExternalId, StudyExternalIdCreate, StudyExternalIdSearchResults]):
    ...
study_external_id_crud = CRUDStudyExternalId(StudyExternalId)