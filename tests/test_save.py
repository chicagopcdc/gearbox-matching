import pytest
import respx

from starlette.config import environ
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


@respx.mock
@pytest.mark.parametrize(
    "data", [ 
        { 'data': [ {'id': 4, 'value': 'steve'} ] }
    ]
)

def test_create(setup_database, client, valid_upload_file_patcher, data):
    """
    Test create /user-input response for a valid user with authorization and
    valid input, ensure correct response.
    """
    fake_jwt = "1.2.3"
    resp = client.post(
        "/user-input", json=data, headers={"Authorization": f"bearer {fake_jwt}"}
    )
    full_res = resp.json()

    resp.raise_for_status()

    res = resp.json().get("results")
    id = resp.json().get("id") 

    assert str(resp.status_code).startswith("20")
    assert resp.json().get("results") == data.get("data", {})
    assert resp.json().get("id") is not None

@respx.mock
def test_get_last_saved_input(setup_database, client):
    """
    Test that the /user-input endpoint returns a 200 and the id of the latest saved obj
    """
    fake_jwt = "1.2.3"
    resp = client.get("/user-input/latest", headers={"Authorization": f"bearer {fake_jwt}"})
    assert resp.status_code == 200
    assert resp.json().get("id")  is not None 

"""
@respx.mock
def test_db_select_input(client, connection):
    fake_jwt = "1.2.3"
    resp = client.get("/user-input/latest", headers={"Authorization": f"bearer {fake_jwt}"})
    # import model

    Session = sessionmaker(bind=connection)
    session = Session()
    si = session.query(SavedInput).first()
    session.close()
    
    assert resp.status_code == 200
    assert resp.json().get("id")  is not None 
"""