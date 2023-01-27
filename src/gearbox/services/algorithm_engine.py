import json

def validate_algorithm_logic_ids():
    """
    description:
        The purpose of this function is to QC the el_criteria_has_criterion ids
        in the ALGORITHM_ENGINE.algorithm_logic json. It checks each
        el_criteria_has_criterion.id in the algorithm_logic json to validate 
        that it exists in the list of el_criteria_has_criterion ids 
        related to the study_version for which the algorithm_engine is being
        stored.

    args:
        algorithm_logic json
        study_version_id
    """
    pass

def validate_algorithm_logic_unique()
    """
    description:
        The purpose of this function is to ensure that there is no logically 
        duplicate algorithm_logic json for a particular study version
        in the algorithm_engine table.
    """
    pass
