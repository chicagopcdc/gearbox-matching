import pytest
from sqlalchemy.orm import sessionmaker 
from gearbox.models import StudyVersion
from .test_utils import is_aws_url

@pytest.mark.parametrize(
    "data", [ 
        {
            "study_version": 
            {
                "study_id": 1,
                "active": True
            },
            "study_algorithm_engine": 
            {
                "study_version_id": 7,
                "eligibility_criteria_id": 7,
                "algorithm_logic": None,
                "algorithm_version": 1,
                "logic_file": "./tests/data/new_algorithm_logic.json",
                "test": "create_new_study_algorithm_engine"
            },
        }
    ]
)
def test_create_study_version_eligibility_criteria(setup_database, client, data, connection):
    fake_jwt = "1.2.3"

    logic_file = "./tests/data/new_algorithm_logic.json"
    with open(logic_file, 'r') as comp_file:
        ae_logic_json = comp_file.read().replace('\n','').replace('\t',' ')

    test_data = {
        "study_algorithm_engine": {
            "study_version_id": 7,
            "eligibility_criteria_id": 7,
            "algorithm_version": 1,
            "algorithm_logic": ae_logic_json
        },
        "eligibility_criteria_info_id": 1
    }


    resp = client.post("/study-version-study-algorithm", json=test_data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    """
    errors = []
    try: 
        Session = sessionmaker(bind=connection)
        db_session = Session()
        study_version = db_session.query(StudyVersion).filter(StudyVersion.study_id==data['study_id']).first()
        if not study_version: 
            errors.append(f"Study_version for study id: {data['study_id']} not created")

        active_study_versions = db_session.query(StudyVersion).filter(StudyVersion.study_id==data['study_id']).filter(StudyVersion.active==True).all()
        if len(active_study_versions) != 1:
            errors.append(f"Study id: {data['study_id']} has {len(active_study_versions)} active study versions, should have exactly 1.")

    except Exception as e:
        errors.append(f"Test study_version unexpected exception: {str(e)}")
    if not str(resp.status_code).startswith("20"):
        errors.append(f"Invalid https status code returned from test_create_study_version: {resp.status_code} ")

    assert not errors, "errors occurred: \n{}".format("\n".join(errors))
    """