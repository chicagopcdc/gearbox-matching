from .base import CRUDBase
from gearbox.models import SiteHasStudy
from gearbox.schemas import SiteHasStudyCreate, SiteHasStudySearchResults

class CRUDSiteHasStudy(CRUDBase [SiteHasStudy, SiteHasStudyCreate, SiteHasStudySearchResults]):
    ...
site_has_study_crud = CRUDSiteHasStudy(SiteHasStudy)