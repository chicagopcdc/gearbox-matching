import importlib
import json
from collections import defaultdict

import pytest
from alembic.config import main
import httpx
import respx
from starlette.config import environ
from starlette.testclient import TestClient

from unittest.mock import MagicMock, patch
import asyncio

environ["TESTING"] = "TRUE"
from mds import config
from mds.agg_mds import datastore


# NOTE: AsyncMock is included in unittest.mock but ONLY in Python 3.8+
class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


@pytest.fixture(autouse=True, scope="session")
def setup_test_database():
    from mds import config

    main(["--raiseerr", "upgrade", "head"])

    yield

    importlib.reload(config)
    if not config.TEST_KEEP_DB:
        main(["--raiseerr", "downgrade", "base"])


@pytest.fixture()
def client():
    from mds import config
    from mds.main import get_app

    importlib.reload(config)

    with TestClient(get_app()) as client:
        yield client


@pytest.fixture(
    params=[
        "dg.TEST/87fced8d-b9c8-44b5-946e-c465c8f8f3d6",
        "87fced8d-b9c8-44b5-946e-c465c8f8f3d6",
    ]
)
def guid_mock(request):
    """
    Yields guid mock.
    """
    yield request.param


@pytest.fixture()
def signed_url_mock():
    """
    Yields signed url mock.
    """
    yield "https://mock-signed-url"




@pytest.fixture(scope="function")
def valid_upload_file_patcher(client, guid_mock, signed_url_mock):
    patches = []

    access_token_mock = MagicMock()
    patches.append(patch("authutils.token.fastapi.access_token", access_token_mock))
    patches.append(patch("mds.save.access_token", access_token_mock))

    async def get_access_token(*args, **kwargs):
        return {"sub": "1"}

    access_token_mock.return_value = get_access_token

    for patched_function in patches:
        patched_function.start()

    yield {
        "access_token_mock": access_token_mock,
    }

    for patched_function in patches:
        patched_function.stop()


















