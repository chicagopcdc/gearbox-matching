import importlib
import json
from collections import defaultdict
import tempfile

import pytest
# from pytest_postgresql import factories

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import Engine

from alembic.config import main
import httpx
import respx
from starlette.config import environ
from starlette.testclient import TestClient

from unittest.mock import MagicMock, patch
import asyncio

from gearbox import config
# from gearbox.models import base_class, study
from gearbox.models import Base, Study

class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

"""
    N O T E: as of 04/25/2022 
    pytest-postgresql requires psycopg3, and the current version
    of sqlalchemy is still using psycopg2. Once Sqlalchemy 2.0 is available, 
    we can leverage pytest-postgresql in the test scripts. 

socket_dir = tempfile.TemporaryDirectory()

postgresql_my_proc = factories.postgresql_proc(
    port=config.DB_PORT,
    user=config.DB_USER,
    password="",
    dbname=config.DB_DATABASE,
    host=config.DB_HOST,
    unixsocketdir=socket_dir.name
)

postgresql_my = factories.postgresql('postgresql_my_proc')
print(f"POSTGRESQL_MY TYPE: {type(postgresql_my)}")
"""

@pytest.fixture(scope="session")
def connection():
    engine = create_engine(config.ALEMBIC_DB_STRING)
    return engine.connect()

def file_to_table(conn, cursor, table_name, file_name):
    with open(file_name, 'r') as f:
        copy_sql = "COPY " + table_name + " FROM stdin DELIMITER E'\t' CSV HEADER"
        cursor.copy_expert(sql=copy_sql, file=f)

@pytest.fixture(scope="session")
def setup_database(connection) -> Engine:

    Session = sessionmaker(bind=connection)
    session = Session()

    main(["--raiseerr","downgrade","base"])
    main(["--raiseerr","upgrade","head"])


    cursor = session.connection().connection.cursor()
    conn = session.connection().connection


    # COPY DATA INTO TABLES
    file_to_table(conn, cursor,'study', './postgres-data/td_study.tsv')
    file_to_table(conn, cursor,'study_version', './postgres-data/td_study_version.tsv')
    file_to_table(conn, cursor,'value', './postgres-data/td_value.tsv')
    file_to_table(conn, cursor,'input_type', './postgres-data/td_input_type.tsv')
    file_to_table(conn, cursor,'tag', './postgres-data/td_tag.tsv')
    file_to_table(conn, cursor,'criterion', './postgres-data/td_criterion.tsv')
    file_to_table(conn, cursor,'criterion_has_value', './postgres-data/td_criterion_has_value.tsv')
    file_to_table(conn, cursor,'eligibility_criteria', './postgres-data/td_eligibility_criteria.tsv')
    file_to_table(conn, cursor,'display_rules', './postgres-data/td_display_rules.tsv')
    file_to_table(conn, cursor,'triggered_by', './postgres-data/td_triggered_by.tsv')
    file_to_table(conn, cursor,'criterion_has_tag', './postgres-data/td_criterion_has_tag.tsv')
    file_to_table(conn, cursor,'el_criteria_has_criterion', './postgres-data/td_el_criteria_has_criterion.tsv')
    file_to_table(conn, cursor,'study_algorithm_engine', './postgres-data/td_study_algorithm_engine.tsv')
    file_to_table(conn, cursor,'algorithm_engine', './postgres-data/td_algorithm_engine.tsv')
    conn.commit()

    yield session
    session.close()


@pytest.fixture(scope="session")
def client(event_loop):
    from gearbox import config
    from gearbox.main import get_app

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
    patches.append(patch("gearbox.routers.user_input.access_token", access_token_mock))

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


@pytest.yield_fixture(scope="session")
def event_loop(request):
    # Create an instance of the default event loop for each test
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

