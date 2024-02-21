import importlib
from collections import OrderedDict
import json
import os
import glob
from datetime import datetime
import re
from json import JSONEncoder
from collections import defaultdict
import tempfile

import pytest
# from pytest_postgresql import factories

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
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
# from gearbox.models import Base, Study
# from gearbox.models import Base

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
    file_to_table(conn, cursor,'source', './postgres-data/td_source.tsv')
    file_to_table(conn, cursor,'study', './postgres-data/td_study.tsv')
    file_to_table(conn, cursor,'study_links', './postgres-data/td_study_links.tsv')
    file_to_table(conn, cursor,'site', './postgres-data/td_site.tsv')
    file_to_table(conn, cursor,'site_has_study', './postgres-data/td_site_has_study.tsv')
    file_to_table(conn, cursor,'study_version', './postgres-data/td_study_version.tsv')
    file_to_table(conn, cursor,'study_algorithm_engine', './postgres-data/td_study_algorithm_engine.tsv')
    file_to_table(conn, cursor,'unit', './postgres-data/td_unit.tsv')
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
    # file_to_table(conn, cursor,'study_algorithm_engine', './postgres-data/td_study_algorithm_engine.tsv')
    conn.commit()

    # cursor.execute("SELECT setval('algorithm_engine_id_seq', (SELECT MAX(id) FROM algorithm_engine));")
    cursor.execute("SELECT setval('criterion_id_seq', (SELECT MAX(id) FROM criterion));")
    cursor.execute("SELECT setval('display_rules_id_seq', (SELECT MAX(id) FROM display_rules));")
    cursor.execute("SELECT setval('el_criteria_has_criterion_id_seq', (SELECT MAX(id) FROM el_criteria_has_criterion));")
    cursor.execute("SELECT setval('eligibility_criteria_id_seq', (SELECT MAX(id) FROM eligibility_criteria));")
    cursor.execute("SELECT setval('input_type_id_seq', (SELECT MAX(id) FROM input_type));")
    cursor.execute("SELECT setval('site_id_seq', (SELECT MAX(id) FROM site));")
    cursor.execute("SELECT setval('study_id_seq', (SELECT MAX(id) FROM study));")
    cursor.execute("SELECT setval('study_algorithm_engine_id_seq', (SELECT MAX(id) FROM study_algorithm_engine));")
    cursor.execute("SELECT setval('study_links_id_seq', (SELECT MAX(id) FROM study_links));")
    cursor.execute("SELECT setval('study_version_id_seq', (SELECT MAX(id) FROM study_version));")
    cursor.execute("SELECT setval('tag_id_seq', (SELECT MAX(id) FROM tag));")
    cursor.execute("SELECT setval('triggered_by_id_seq', (SELECT MAX(id) FROM triggered_by));")
    cursor.execute("SELECT setval('value_id_seq', (SELECT MAX(id) FROM value));")
    cursor.execute("SELECT setval('unit_id_seq', (SELECT MAX(id) FROM unit));")
    file_to_table(conn, cursor,'eligibility_criteria_info', './postgres-data/td_eligibility_criteria_info.tsv')
    cursor.execute("SELECT setval('eligibility_criteria_info_id_seq', (SELECT MAX(id) FROM eligibility_criteria_info));")
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

@pytest.fixture
def mock_new_criterion():

    class MockNewCriterion(object):
        code = "test_criteria"
        display_name = "this is a test criterion"
        description = "test is a test criterion"
        active = False
        input_type_id = 1
        tags = [1]
        values = [3]
        display_rules_priority = 1001
        display_rules_version = 5
        triggered_by_criterion_id = 1
        triggered_by_value_id = 1
        triggered_by_path = "2.3.4"

        def to_json(self):
            return {
                "code": self.code,
                "display_name": self.display_name,
                "description": self.description,
                "active": self.active,
                "input_type_id": self.input_type_id,
                "tags": self.tags,
                "values": self.values,
                "display_rules_priority": self.display_rules_priority,
                "display_rules_version": self.display_rules_version,
                "triggered_by_criterion_id": self.triggered_by_criterion_id,
                "triggered_by_value_id": self.triggered_by_value_id,
                "triggered_by_path": self.triggered_by_path
            }
    return MockNewCriterion()
