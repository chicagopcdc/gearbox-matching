import pytest
import random

from sqlalchemy.orm import sessionmaker

from gearbox.models import Criterion, CriterionHasTag, CriterionHasValue, DisplayRules, TriggeredBy

from starlette.config import environ

from gearbox import config

def test_get_criterion(setup_database, client):

    fake_jwt = "1.2.3"
    resp = client.get(f"/criterion/1", headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")

def test_get_criteria_not_exist_in_match_form(setup_database, client):

    fake_jwt = "1.2.3"
    resp = client.get(f"/criteria-not-exist-in-match-form", headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")
    full_res = resp.json()
    print(f"FULL RES: {full_res}")