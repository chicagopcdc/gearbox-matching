import requests
import json

host = 'http://0.0.0.0:5000'
headers = {'Content-type': 'application/json'}

############################

def compose_studies():
    json_data=[]
    data = [
        'APAL2020SC',
        'AAML2112',
        'APAL2020B',
        'APAL2020C',
        'APAL2020D',
        'AAML20XX',
        'APAL2020F',
        'APAL2020G',
    ]
    for item in data:
        json_data.append(json.dumps({'name': item, 'code': item, 'active': 0}))

    return json_data



##########################################

def run ():

    #studies
    studies = compose_studies()
    for study in studies:
        response = requests.post('{}/study/create_study'.format(host), data = study, headers = headers)
        #print (response.text)
    response = requests.get('{}/study/info'.format(host), headers = headers)
    print (response.text)


    #study_versions

    map_study2version = {}

    for study in studies:
        study_code = json.loads(study)['code']
        response = requests.get('{}/study/{}'.format(host, study_code))
        resp_txt = json.loads(response.text)        
        id = int(resp_txt['id'])
        data = {
            'study_id': id,
            'active': 0
        }
        json_data = json.dumps(data)
        
        response = requests.post('{}/study_version/create_study_version'.format(host), data = json_data, headers = headers)
        #print (response.text)
        
    response = requests.get('{}/study_version/info'.format(host), headers = headers)
    print (response.text)
    

    
    
if __name__ == '__main__':
    run()
