import pytest
from sqlalchemy.orm import sessionmaker 
from gearbox.models import StudyVersion
from .test_utils import is_aws_url

@pytest.mark.parametrize(
    "data", [ 
        {
            "study_algorithm_engine": 
            {
                "study_version_id": 7,
                "eligibility_criteria_id": 7,
                "algorithm_logic": None,
                "algorithm_version": 1,
                "algorithm_logic": None,
                "test": "create_new_study_algorithm_engine"
            },
            "eligibility_criteria_info_id": 1
        }
    ]
)
def test_create_study_version_eligibility_criteria(setup_database, client, data, connection):
    fake_jwt = "1.2.3"

    logic_file = "./tests/data/new_algorithm_logic.json"
    with open(logic_file, 'r') as comp_file:
        ae_logic_json = comp_file.read().replace('\n','').replace('\t',' ')

    data["study_algorithm_engine"]["algorithm_logic"] = ae_logic_json

    resp = client.post("/study-version-study-algorithm", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()