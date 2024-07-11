from enum import Enum

class EligibilityCriteriaInfoStatus(Enum):
    ACTIVE = 'ACTIVE'
    IN_PROCESS = 'IN_PROCESS'
    INACTIVE = 'INACTIVE'

class EligibilityCriteriaStatus(Enum):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    IN_PROCESS = 'IN_PROCESS'
    INACTIVE = 'INACTIVE'

class CriteriaStagingStatus(Enum):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    IN_PROCESS = 'IN_PROCESS'
    INACTIVE = 'INACTIVE'