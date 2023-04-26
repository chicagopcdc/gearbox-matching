from .base import CRUDBase
from gearbox.models import Tag
from gearbox.schemas import TagCreate, TagSearchResults

class CRUDTag(CRUDBase [Tag, TagCreate, TagSearchResults]):
    ...
tag_crud = CRUDTag(Tag)