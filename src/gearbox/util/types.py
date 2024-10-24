from enum import Enum

class StudyVersionStatus(Enum):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    IN_PROCESS = 'IN_PROCESS'
    INACTIVE = 'INACTIVE'

class EligibilityCriteriaStatus(Enum):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    IN_PROCESS = 'IN_PROCESS'
    INACTIVE = 'INACTIVE'

class AdjudicationStatus(Enum):
    NEW = 'NEW'
    EXISTING = 'EXISTING'
    ACTIVE = 'ACTIVE'
    IN_PROCESS = 'IN_PROCESS'
    INACTIVE = 'INACTIVE'

class EchcAdjudicationStatus(Enum):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    IN_PROCESS = 'IN_PROCESS'
    INACTIVE = 'INACTIVE'