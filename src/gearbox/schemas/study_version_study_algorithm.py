from gearbox.schemas import StudyAlgorithmEngineCreateInput, StudyAlgorithmEngineCreate, StudyAlgorithmEngine
from pydantic import BaseModel

class StudyVersionStudyAlgorithmBase(BaseModel):
    study_algorithm_engine: StudyAlgorithmEngineCreateInput

class StudyVersionStudyAlgorithmCreate(StudyVersionStudyAlgorithmBase):
    eligibility_criteria_info_id: int

class StudyVersionStudyAlgorithm(StudyVersionStudyAlgorithmBase):
    # study_algorithm_engine: StudyAlgorithmEngineCreate
    eligibility_criteria_info_id: int
    study_algorithm_engine: StudyAlgorithmEngine

StudyVersionStudyAlgorithm, StudyVersionStudyAlgorithmCreate