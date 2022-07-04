import pytest

from gearbox import config
from gearbox.models import Base, Study

def test_database(setup_database):

    print(f"DB STRING: {config.ALEMBIC_DB_STRING}")
    session = setup_database

    assert len(session.query(Study).all()) == 8

def test_insert_study(setup_database):

    new_study = Study(id=9, name='test from pytest', code='1111', active=True)
    session = setup_database
    session.add(new_study)
    assert len(session.query(Study).all()) == 9

    try:
        # session.commit()
        session.rollback()
    except:
        raise Exception

