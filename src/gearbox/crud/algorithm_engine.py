from .base import CRUDBase
from gearbox.models import AlgorithmEngine
from gearbox.schemas import AlgorithmEngineCreate, AlgorithmEngineSearchResults

class CRUDAlgorithmEngine(CRUDBase [AlgorithmEngine, AlgorithmEngineCreate, AlgorithmEngineSearchResults]):
    ...
algorithm_engine_crud = CRUDAlgorithmEngine(AlgorithmEngine)

