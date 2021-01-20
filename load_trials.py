import requests
import json

host = 'http://0.0.0.0:5000'
headers = {'Content-type': 'application/json'}

############################

def print_info(table_name):
    response = requests.get('{}/{}/info'.format(host, table_name), headers = headers)
    print ('\n#################################\n\ninfo for table: {}\n'.format(table_name))
    print (response.text)
    print ('\n#################################\n\n')
    
def compose_studies():
    json_data=[]
    data = [
        'APAL2020SC',
        # 'AAML2112',
        # 'APAL2020B',
        # 'APAL2020C',
        # 'APAL2020D',
        # 'AAML20XX',
        # 'APAL2020F',
        # 'APAL2020G',
    ]
    for item in data:
        dict_data = {
            'name': item,
            'code': item,
            'active': 0,
        }
        json_data.append(json.dumps(dict_data))

    return json_data



##########################################

def run ():

    studies = compose_studies()

    for study in studies:

        '''study'''
        response = requests.post('{}/study/create_study'.format(host), data = study, headers = headers)
        if response.status_code in [201, 409]:
            pass
        else:
            print (response.text)


        '''study_versions'''
        
        #get code for study to lookup id
        study_code = json.loads(study)['code']

        #get the id for the study
        response = requests.get('{}/study/{}'.format(host, study_code))
        resp_txt = json.loads(response.text)
        study_id = int(resp_txt['id'])
        data = {
            'study_id': study_id,
            'active': 0
        }
        json_data = json.dumps(data)
        
        response = requests.post('{}/study_version/create_study_version'.format(host), data = json_data, headers = headers)
        if response.status_code in [201, 409]:
            pass
        else:
            print (response.status_code)
        

        '''eligibility_criteria'''

        #get the study_version_id
        response = requests.get('{}/study_version/{}'.format(host, study_id))
        resp_txt = json.loads(response.text)
        study_version_id = int(resp_txt['id'])

        data = {
            'active': 0,
            'study_version_id': study_version_id,
        }
        json_data = json.dumps(data)

        response = requests.post('{}/eligibility_criteria/create_eligibility_criteria'.format(host), data = json_data, headers = headers)
        if response.status_code in [201, 409]:
            pass
        else:
            print (response.status_code)


        '''input_type'''

        input_type_name = 'Age'
        data= {
            'type': 'text_field',
            'name': input_type_name,
        }
        json_data = json.dumps(data)

        response = requests.post('{}/input_type/create_input_type'.format(host), data = json_data, headers = headers)
        if response.status_code in [201, 409]:
            pass
        else:
            print (response.status_code)

        
        # '''ontology_code'''
        # data = {
        #     'ontology_url':,
        #     'name':,
        #     'code':,
        #     'value':,
        #     'version':,
        # }
        
        '''criterion'''

        #lookup input_type_id
        response = requests.get('{}/input_type/{}'.format(host, input_type_name))
        resp_txt = json.loads(response.text)
        input_type_id = int(resp_txt['id'])

        criterion_code = 'Age'
        data = {
            'code': criterion_code,
            'display_name': 'Age',
            'description': 'age in years',
            'active': 0,
            'input_type_id': input_type_id,
        }
        json_data = json.dumps(data)
        
        response = requests.post('{}/criterion/create_criterion'.format(host), data = json_data, headers = headers)
        if response.status_code in [201, 409]:
            pass
        else:
            print (response.status_code)


        '''tag'''
        data = {
            'code': 'Age',
            'type': 'Age',
        }
        json_data = json.dumps(data)
        
        response = requests.post('{}/tag/create_tag'.format(host), data = json_data, headers = headers)
        if response.status_code in [201, 409]:
            pass
        else:
            print (response.status_code)

            
        '''value'''

        value_code = 'Age'
        data = {
            'code': value_code,
            'type': 'float',
            'value_string': 'years',
            'upper_threshold': None,
            'lower_threshold': 22,
            'active': 0,
            #'value_list':,
            #'value_bool':,
        }
        json_data = json.dumps(data)
        
        response = requests.post('{}/value/create_value'.format(host), data = json_data, headers = headers)
        if response.status_code in [201, 409]:
            pass
        else:
            print (response.status_code)
        
        
        '''el_criteria_has_criterion'''

        #lookup criterion_id
        response = requests.get('{}/criterion/{}'.format(host, criterion_code))
        resp_txt = json.loads(response.text)
        criterion_id = int(resp_txt['id'])

        #lookup eligibility_criteria_id
        response = requests.get('{}/eligibility_criteria/{}'.format(host, study_version_id))
        resp_txt = json.loads(response.text)
        eligibility_criteria_id = int(resp_txt['id'])

        #lookup value_id
        response = requests.get('{}/value/{}'.format(host, value_code))
        resp_txt = json.loads(response.text)
        value_id = int(resp_txt['id'])

        data = {
            'criterion_id': criterion_id,
            'eligibility_criteria_id': eligibility_criteria_id,
            'active': 0,
            'value_id': value_id,
        }
        json_data = json.dumps(data)

        response = requests.post('{}/el_criteria_has_criterion/create_el_criteria_has_criterion'.format(host), data = json_data, headers = headers)
        if response.status_code in [201, 409]:
            pass
        else:
            print (response.status_code)

        

# def run ():

#     #studies

#     studies = compose_studies()

#     for study in studies:
#         response = requests.post('{}/study/create_study'.format(host), data = study, headers = headers)
#         if response.status_code in [201, 409]:
#             pass
#         else:
#             print (response.text)

#     print_info('study')

#     #study_versions

#     for study in studies:
#         study_code = json.loads(study)['code']

#         #get the id for the study
#         response = requests.get('{}/study/{}'.format(host, study_code))
#         resp_txt = json.loads(response.text)
#         id = int(resp_txt['id'])
#         data = {
#             'study_id': id,
#             'active': 0
#         }
#         json_data = json.dumps(data)
        
#         response = requests.post('{}/study_version/create_study_version'.format(host), data = json_data, headers = headers)
#         if response.status_code in [201, 409]:
#             pass
#         else:
#             print (response.status_code)
        
#     print_info('study_version')
    

#     #eligibility_criteria


#     #get the id for the study
#     response = requests.get('{}/study_version/{}'.format(host, study_code))
#     resp_txt = json.loads(response.text)
#     id = int(resp_txt['id'])
#     data = {
#         'study_id': id,
#         'active': 0
#     }
#     json_data = json.dumps(data)

    
    
if __name__ == '__main__':
    run()
