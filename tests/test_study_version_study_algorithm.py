import pytest
from sqlalchemy.orm import sessionmaker 
from gearbox.models import StudyVersion
from .test_utils import is_aws_url
from sqlalchemy import select, exc
from gearbox.models import StudyAlgorithmEngine, EligibilityCriteriaInfo

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
def test_create_study_version_study_algorithm(setup_database, client, data, connection):
    fake_jwt = "1.2.3"

    logic_file = "./tests/data/new_algorithm_logic.json"
    with open(logic_file, 'r') as comp_file:
        ae_logic_json = comp_file.read().replace('\n','').replace('\t',' ')

    data["study_algorithm_engine"]["algorithm_logic"] = ae_logic_json

    resp = client.post("/study-version-study-algorithm", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    full_res = resp.json()

    new_study_algorithm_engine_id = full_res['study_algorithm_engine']['id']
    new_eligibility_criteria_info_id = full_res['eligibility_criteria_info_id']

    errors = []

    # verify db changes
    try:
        Session = sessionmaker(bind=connection)
        db_session = Session()

        # verify study_algorithm_engine row created
        stmt = select(StudyAlgorithmEngine).where(StudyAlgorithmEngine.id == new_study_algorithm_engine_id)
        nsae = db_session.execute(stmt).first()
        if not nsae:
            errors.append(f"ERROR: create_new_study_version_study_algorithm test failed to confirm new study_algorithm_engine row created.")

        # verify eligibility_criteria_info row created
        stmt = select(EligibilityCriteriaInfo).where(EligibilityCriteriaInfo.study_algorithm_engine_id == new_study_algorithm_engine_id)
        updated_eci = db_session.execute(stmt).first()
        if not updated_eci:
            errors.append(f"ERROR: create_new_study_version_study_algorithm test failed to confirm updated eligibility_criteria_info row.")

        db_session.close()
    except Exception as e:
        errors.append(f"SQL ERROR: create_new_study_version_study_algorithm: {e}")