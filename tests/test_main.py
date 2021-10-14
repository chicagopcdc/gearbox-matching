import gino
import pytest
from unittest.mock import patch
from conftest import AsyncMock


def test_status_success(client):
    patch("mds.main.db.scalar", AsyncMock(return_value="some time")).start()

    resp = client.get("/_status")
    resp.raise_for_status()
    assert resp.status_code == 200
    assert resp.json().get("status") == "OK",



def test_status_error(client):
    patch("mds.main.db.scalar", AsyncMock(side_effect=Exception("some error"))).start()

    try:
        resp = client.get("/_status")
        resp.raise_for_status()
    except:
        assert resp.status_code == 500
        assert resp.json() == {
            "detail": {"message": "database offline", "code": 500}
        }
