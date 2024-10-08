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
def test_get_single_ec(setup_database, client):
    """
    Test create /eligibility_criteria endpoint
    valid input, ensure correct response.
    """
    
    fake_jwt = "1.2.3"
    resp = client.get("/eligibility-criteria/1", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()
    resp.raise_for_status()

@pytest.mark.asyncio
def test_build_ec(setup_database, client):
    """
    Test create /eligibility_criteria endpoint
    valid input, ensure correct response.
    """
    
    fake_jwt = "1.2.3"
    resp = client.post("/build-eligibility-criteria", headers={"Authorization": f"bearer {fake_jwt}"})
    full_res = resp.json()

    resp.raise_for_status()
    ecdata_file = './tests/data/eligibilityCriteria.json'

    """ SERIALIZE STUDIES TO COMPARE AGAINST - UNCOMMENT TO WRITE NEW COMPARE DATA
    with open(ecdata_file,'w') as comp_file:
        json.dump(full_res, comp_file)
    """

    with open(ecdata_file, 'r') as comp_file:
        ec_compare = json.load(comp_file)

    ec = full_res
    ec_compare = ec_compare

    diff = []
    for i in range (len(ec_compare)):
        ec_diff = DeepDiff(ec[i], ec_compare[i], ignore_order=True)
        if ec_diff:
            diff.append(ec_diff)

    assert not diff, f"differences occurred: \n{diff}"

def test_get_ec(setup_database, client):
    errors = []
    fake_jwt = "1.2.3"
    url = client.get("/eligibility-criteria", headers={"Authorization": f"bearer {fake_jwt}"})
    url_str =  url.content.decode('ascii').strip('\"')

    assert is_aws_url(url_str)

@pytest.mark.parametrize(
    "data", [ 
        {
        }
    ]
)
@pytest.mark.asyncio
def test_eligibility_criteria(setup_database, client, data):
    """
    Test create eligibility_criteria
    """
    fake_jwt = "1.2.3"
    resp = client.post("/eligibility-criteria", json=data, headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()

    full_res = resp.json()
    new_ec_id = full_res['id']

    assert str(resp.status_code).startswith("20")
