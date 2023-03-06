from .base import CRUDBase
from gearbox.models import StudyAlgorithmEngine
from gearbox.schemas import StudyAlgorithmEngineCreate, StudyAlgorithmEngineSearchResults

class CRUDStudyAlgorithmEngine(CRUDBase [StudyAlgorithmEngine, StudyAlgorithmEngineCreate, StudyAlgorithmEngineSearchResults]):
    ...
study_algorithm_engine_crud = CRUDStudyAlgorithmEngine(StudyAlgorithmEngine)

