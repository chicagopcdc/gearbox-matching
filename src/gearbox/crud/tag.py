from .base import CRUDBase
from gearbox.models.models import Tag
from ..schemas import TagCreate, TagSearchResults

class CRUDTag(CRUDBase [Tag, TagCreate, TagSearchResults]):
    ...
tag = CRUDTag(Tag)