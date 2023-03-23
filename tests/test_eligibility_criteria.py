from re import A
import pytest
import random
import json
from .test_utils import is_aws_url
from deepdiff import DeepDiff

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from gearbox import config

@pytest.mark.asyncio
def test_build_ec(setup_database, client):
    """
    Test create /eligibility_criteria endpoint
    valid input, ensure correct response.
    """
    
    fake_jwt = "1.2.3"
    resp = client.post("/build-eligibility-criteria-set", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    resp.raise_for_status()
    ecdata_file = './tests/data/eligibilityCriteria.json'

    #""" SERIALIZE STUDIES TO COMPARE AGAINST - UNCOMMENT TO WRITE NEW COMPARE DATA
    # with open(ecdata_file,'w') as comp_file:
    #    json.dump(full_res, comp_file)
    #"""

    with open(ecdata_file, 'r') as comp_file:
        ec_compare = json.load(comp_file)

    ec = full_res['results']
    ec_compare = ec_compare['results']

    print(f"EC: {ec}")
    print("-=================================================")
    print(f"EC_COMPARE: {ec_compare}")

    diff = []
    for i in range (len(ec_compare)):
        ec_diff = DeepDiff(ec[i], ec_compare[i], ignore_order=True)
        if ec_diff:
            diff.append(ec_diff)

    assert not diff, "differences occurred: \n{}".format("\n".join(diff))            

def test_get_ec(setup_database, client):
    errors = []
    fake_jwt = "1.2.3"
    url = client.get("/eligibility-criteria-set", headers={"Authorization": f"bearer {fake_jwt}"})
    url_str =  url.content.decode('ascii').strip('\"')

    assert is_aws_url(url_str)

@pytest.mark.parametrize(
    "data", [ 
        {
        }
    ]
)
@pytest.mark.asyncio
# def test_create_el_criteria_has_criterion(setup_database, client, valid_upload_file_patcher, data):
def test_create_el_criteria_has_criterion(setup_database, client, data):
    """
    Test create el_criteria_has_criterion
    """
    fake_jwt = "1.2.3"
    resp = client.post("/eligibility-criteria", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    full_res = resp.json()
    new_ec_id = full_res['id']

    assert str(resp.status_code).startswith("20")
