def test_get_input_types(setup_database, client):
    """
    Endpoint returns all existing input types from the input_type table. 
    """
    errors = []
    fake_jwt = "1.2.3"
    resp = client.get("/input-types", headers={"Authorization": f"bearer {fake_jwt}"})
    resp.raise_for_status()
    assert str(resp.status_code).startswith("20")