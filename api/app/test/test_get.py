import pytest

from app.main.model.study import Study
from app.main.controller.study_controller import Create, AllStudiesInfo, StudyInfo

@pytest.fixture(scope="function")
def studyA():
    return Study(name = 'studyA', code = 'codeA', active = 0)

@pytest.fixture(scope="function")
def studyB():
    return Study(name = 'studyB', code = 'codeB', active = 0)

def test_create_study(studyA, studyB, app, session):
    session.add(studyA)
    session.add(studyB)
    session.commit()

    payload= {'name': 'thisName', 'code': 'thisCode', 'active': 0}

    with app.test_request_context("/study/create_study", method="POST", json=payload):
        response, status_code = Create().post()
        print (response)
        assert status_code == 201

    with app.test_request_context("/study/info", method="GET"):        
        response = AllStudiesInfo().get()
        print (response)
        table_data = response.json['body']
        for item in table_data:
            print (item) #response.json['body'])
        assert response.status_code == 200
        #assert response.status_code == 201
