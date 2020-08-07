import json
import os
import requests
import unittest

from app.main import db

headers = {'content-type': 'application/json'}


class TestStudy(unittest.TestCase):

    def test_00_info(self):
        #remove the db file for clean-slate testing
        os.remove('/docker-flask/app/test/flask_boilerplate_test.db')

        #test that /info gives 500 (no db)
        response = requests.get('http://0.0.0.0:5000/study/info')
        self.assertEqual(response.status_code, 500)
        
        #establish the db, and check /info again (db yes, but no data yet)
        db.Model.metadata.create_all(db.engine)
        response = requests.get('http://0.0.0.0:5000/study/info')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text)['body'],[]) #<-table should be empty
        
    def test_01_create(self):
        #create rows in the study table
        payloads = [
            {'name': 'thisName', 'code': 'thisCode', 'active': 0},
            {'name': 'thatName', 'code': 'thatCode', 'active': 0},
            {'name': 'theName', 'code': 'theCode', 'active': 0}
        ]
        for payload in payloads:
            response = requests.post(
                'http://0.0.0.0:5000/study/create_study',
                headers=headers,
                json=payload,
            )
            self.assertEqual(response.status_code, 201) #<-201/created

        #verify that the data is there by comparing /info with payload
        response = requests.get('http://0.0.0.0:5000/study/info')
        self.assertEqual(response.status_code, 200)
        body_list = json.loads(response.text)['body']
        for payload in payloads:
            code = payload['code']
            for body in body_list: #<-prune down body list, as payload items are verified
                if body['code']==code:
                    body_list.remove(body)
        self.assertEqual(body_list,[])

    def test_02_update(self):
        payload = {'code': 'duplicateCode'}
        #change the stdy code for some studies; attempt to set them both to the same code
        for code in ['thisCode', 'thatCode']:
            response = requests.put(
                'http://0.0.0.0:5000/study/update_study/{}'.format(code),
                headers=headers,
                json=payload,
            )
            if code == 'thisCode':
                self.assertEqual(response.status_code, 200) #<- code updated from 'thisCode' to 'duplicateCode'
            elif code =='thatCode':
                self.assertEqual(response.status_code, 409) #<- expecting duplicate code error

    def test_03_delete(self):
        code='duplicateCode'
        response = requests.delete('http://0.0.0.0:5000/study/delete_study/{}'.format(code))
        self.assertEqual(response.status_code, 200)
        
        code='doesNotExist'
        response = requests.delete('http://0.0.0.0:5000/study/delete_study/{}'.format(code))
        self.assertEqual(response.status_code, 404) #<- not found: study with code="doesNotExist"

                
if __name__ == '__main__':
    unittest.main()
