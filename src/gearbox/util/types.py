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
    CRITERIA_ADJUDICATION = 'CRITERIA_ADJUDICATION'
    ECHC_ADJUDICATION = 'ECHC_ADJUDICATION'

class CriterionStagingStatus(Enum):
    NEW = 'NEW'
    EXISTING = 'EXISTING'
    ACTIVE = 'ACTIVE'
    IN_PROCESS = 'IN_PROCESS'
    INACTIVE = 'INACTIVE'