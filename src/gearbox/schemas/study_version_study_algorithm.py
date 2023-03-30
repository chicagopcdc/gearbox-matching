from gearbox.schemas import StudyVersionCreate, StudyAlgorithmEngineCreateInput
from pydantic import BaseModel

class StudyVersionStudyAlgorithmBase(BaseModel):
    eligibility_criteria_info_id: int
    study_algorithm_engine: StudyAlgorithmEngineCreateInput

class StudyVersionStudyAlgorithmCreate(StudyVersionStudyAlgorithmBase):
    pass

class StudyVersionStudyAlgorithm(StudyVersionStudyAlgorithmBase):
    pass


StudyVersionStudyAlgorithm, StudyVersionStudyAlgorithmCreate