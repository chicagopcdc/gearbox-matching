from .base import CRUDBase
from gearbox.models import StudyLink
from gearbox.schemas import StudyLinkSearchResults, StudyLinkCreate

class CRUDStudyLink(CRUDBase [StudyLink, StudyLinkCreate, StudyLinkSearchResults]):
    ...
study_link_crud = CRUDStudyLink(StudyLink)