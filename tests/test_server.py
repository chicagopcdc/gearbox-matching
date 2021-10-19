import time

import pytest
import starlette
from asyncpg import InvalidCatalogNameError
from requests import ReadTimeout
from starlette.testclient import TestClient

from gearbox.main import db
from gearbox.main import get_app


def test_version(client):
    client.get("/version").raise_for_status()


def test_status(client):
    try:
        client.get("/_status").raise_for_status()
    except:
        pass


def test_wait_for_db(monkeypatch):
    monkeypatch.setitem(db.config, "retry_limit", 0)
    monkeypatch.setattr(db.config["dsn"], "database", "non_exist")

    start = time.time()
    with pytest.raises(InvalidCatalogNameError, match="non_exist"):
        with TestClient(get_app()) as client:
            client.get("/_status").raise_for_status()
    assert time.time() - start < 1

    monkeypatch.setitem(db.config, "retry_limit", 2)

    start = time.time()
    with pytest.raises(InvalidCatalogNameError, match="non_exist"):
        with TestClient(get_app()) as client:
            client.get("/_status").raise_for_status()
    assert time.time() - start > 1
