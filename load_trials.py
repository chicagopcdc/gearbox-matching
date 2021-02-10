import json

import numpy as np
import pandas as pd
import requests

############################

data_path = '~/Desktop/tables/'
host = 'http://0.0.0.0:5000'
headers = {'Content-type': 'application/json'}

############################

def create(table, ignore):
    print (table)
    filename = data_path + table + '.csv'
    df = pd.read_csv(filename)
    cols = df.columns
    for index, row in df.iterrows():
        payload = dict(row)
        if ignore:
            discard =[payload.pop(key) for key in ignore]
        for key, val in payload.items():
            if isinstance(val, str):
                pass
            elif pd.isnull(val):
                payload.update({key: None})
            elif isinstance(val, (np.integer)): #needed to allow json serialization
                payload.update({key: val.item()})
        json_payload = json.dumps(payload)
        print (json_payload)
        response = requests.post('{}/{}/create_{}'.format(host, table, table), data = json_payload, headers = headers)
        if response.status_code in [201, 409]:
            print ('success: {}'.format(response.status_code))
        else:
            #print (dir(response))
            print (response.status_code)
    print ('\n\n')

########################################################


#create('study', ['id', 'create_date'])
#create('study_version', ['id', 'create_date'])
#create('value', ['id'])
#create('input_type', ['id'])
#create('tag', ['id'])
#create('criterion', ['id'])
#create('criterion_has_tag', None)

#create('eligibility_criteria', ['id', 'create_date'])
create('el_criteria_has_criterion', ['id'])

#create('algorithm_engine', None)
#create('study_algorithm_engine', None)
#create('eligibility_criteria', ['id', 'create_date'])


########################################################












# table = 'value'
# ignore = ['id']
# print (table)
# filename = data_path + table + '.csv'
# df = pd.read_csv(filename)
# cols = df.columns
# for index, row in df.iterrows():
#     payload = dict(row)
#     discard =[payload.pop(key) for key in ignore]
#     for key, val in payload.items():
#         if pd.isnull(val):
#             payload.update({key: None})
#     json_payload = json.dumps(payload)
#     print (json_payload)
#     response = requests.post('{}/{}/create_{}'.format(host, table, table), data = json_payload, headers = headers)
#     if response.status_code in [201, 409]:
#         pass
#     else:
#         print (response.text)
# print ('\n\n')


#create('eligibility_criteria', ['id', 'create_date'])
#create('study_algorithm_engine', ['date_from', 'Unnamed: 4'])


# print (table)
# filename = data_path + table + '.csv'
# df = pd.read_csv(filename)
# cols = df.columns
# for index, row in df.iterrows():
#     payload = dict(row)
#     discard =[payload.pop(key) for key in ignore]
#     json_payload = json.dumps(payload)
#     print (json_payload)
#     response = requests.post('{}/{}/create_{}'.format(host, table, table), data = json_payload, headers = headers)
#     if response.status_code in [201, 409]:
#         pass
#     else:
#         print (response.text)
# print ('\n\n')







# def print_info(table_name):
#     response = requests.get('{}/{}/info'.format(host, table_name), headers = headers)
#     print ('\n#################################\n\ninfo for table: {}\n'.format(table_name))
#     print (response.text)
#     print ('\n#################################\n\n')

    
# def compose_studies():
#     json_data=[]
#     data = [
#         'APAL2020SC',
#         # 'AAML2112',
#         # 'APAL2020B',
#         # 'APAL2020C',
#         # 'APAL2020D',
#         # 'AAML20XX',
#         # 'APAL2020F',
#         # 'APAL2020G',
#     ]
#     for item in data:
#         dict_data = {
#             'name': item,
#             'code': item,
#             'active': 0,
#         }
#         json_data.append(json.dumps(dict_data))

#     return json_data


# def lookup_an_id(table_name, lookup):
#     response = requests.get('{}/{}/{}'.format(host, table_name, lookup))
#     resp_txt = json.loads(response.text)
#     return int(resp_txt['id'])    


# ##########################################

# DF = pd.read_csv(criteria_path)

# cols = DF.columns
# raw_tags = list(DF[cols[0]])
# tags=[]
# for i in range(0,len(raw_tags)):
#     tag = raw_tags[i]
#     if pd.isnull(tag) or tag=='Eligibility': #<-'Eligibility is a header, not a tag'
#         pass
#     else:
#        tags.append(tag)

# col_studies = []
# studies = []
# for i in range(1,len(cols)):
#     col_studies.append(cols[i])
#     studies.append(cols[i].split('\n')[0])
# study2col = {studies[i]: col_studies[i] for i in range(len(studies))}

# #get row ranges for tags
# df = DF[cols[0]] #this is the first, Unnamed col, where tags are
# q=[0]*len(df)
# for i in range(0,len(df)):
#     if df[i] in tags:
#         q[i]=1
# Q = np.cumsum(q)
# DF['Q'] = Q

# #master eligibility criteria [tag][study]
# EC = {} 
# for tag in tags:
# #DEBUG
# #for tag in ['Age']:
#     EC.update({tag: {}})

#     for study in studies:
#     #DEBUG
#     #for study in ['APAL2020SC']:
#         idx = raw_tags.index(tag)
#         mask = DF['Q'] == idx
#         try:
#             criteria = DF[mask][study2col[study]].values[0].strip('·\xa0\xa0 ')
#         except:
#             criteria = np.nan

#         #DEBUG
#         # print (tag)
#         # print (study)
#         # print(criteria)
#         # print ('\n\n')

#         current_tag_dict = EC.get(tag)
#         current_list = current_tag_dict.get(study)
#         if current_list:
#             new_list = current_list.append(criteria)
#         else:
#             new_list = [criteria]
#         EC[tag].update({study: new_list})
        
# # for col in cols[1::]:
# #     QQ=Q
# #     df = DF[col]
# #     i=0
# #     for item in df:
# #         print('{}:{}'.format(i, item))

               
# #         i+=1
#         #if row[col] in tags:
#         #    print (row[col])




# #def run ():
    
#     # studies = compose_studies()

#     # for study in studies:

#     #     '''study'''
#     #     response = requests.post('{}/study/create_study'.format(host), data = study, headers = headers)
#     #     if response.status_code in [201, 409]:
#     #         pass
#     #     else:
#     #         print (response.text)


#     #     '''study_versions'''       
#     #     study_code = json.loads(study)['code']
#     #     study_id = lookup_an_id('study', study_code)
#     #     data = {
#     #         'study_id': study_id,
#     #         'active': 0
#     #     }
#     #     json_data = json.dumps(data)
#     #     response = requests.post('{}/study_version/create_study_version'.format(host), data = json_data, headers = headers)
#     #     if response.status_code in [201, 409]:
#     #         pass
#     #     else:
#     #         print (response.status_code)
        

#     #     '''eligibility_criteria'''
#     #     study_version_id = lookup_an_id('study_version', study_id)
#     #     data = {
#     #         'active': 0,
#     #         'study_version_id': study_version_id,
#     #     }
#     #     json_data = json.dumps(data)
#     #     response = requests.post('{}/eligibility_criteria/create_eligibility_criteria'.format(host), data = json_data, headers = headers)
#     #     if response.status_code in [201, 409]:
#     #         pass
#     #     else:
#     #         print (response.status_code)


#     #     '''input_type'''
#     #     input_type_name = 'Age'
#     #     data= {
#     #         'type': 'text_field',
#     #         'name': input_type_name,
#     #     }
#     #     json_data = json.dumps(data)
#     #     response = requests.post('{}/input_type/create_input_type'.format(host), data = json_data, headers = headers)
#     #     if response.status_code in [201, 409]:
#     #         pass
#     #     else:
#     #         print (response.status_code)

        
#     #     # '''ontology_code'''
#     #     #
#     #     # data = {
#     #     #     'ontology_url':,
#     #     #     'name':,
#     #     #     'code':,
#     #     #     'value':,
#     #     #     'version':,
#     #     # }

        
#     #     '''criterion'''
#     #     input_type_id = lookup_an_id('input_type', input_type_name)
#     #     criterion_code = 'Age'
#     #     data = {
#     #         'code': criterion_code,
#     #         'display_name': 'Age',
#     #         'description': 'age in years',
#     #         'active': 0,
#     #         'input_type_id': input_type_id,
#     #     }
#     #     json_data = json.dumps(data)
#     #     response = requests.post('{}/criterion/create_criterion'.format(host), data = json_data, headers = headers)
#     #     if response.status_code in [201, 409]:
#     #         pass
#     #     else:
#     #         print (response.status_code)


#     #     '''tag'''
#     #     data = {
#     #         'code': 'Age',
#     #         'type': 'Age',
#     #     }
#     #     json_data = json.dumps(data)
#     #     response = requests.post('{}/tag/create_tag'.format(host), data = json_data, headers = headers)
#     #     if response.status_code in [201, 409]:
#     #         pass
#     #     else:
#     #         print (response.status_code)

            
#     #     '''value'''
#     #     value_code = 'Age'
#     #     data = {
#     #         'code': value_code,
#     #         'type': 'float',
#     #         'value_string': 'years',
#     #         'upper_threshold': None,
#     #         'lower_threshold': 22,
#     #         'active': 0,
#     #         #'value_list':,
#     #         #'value_bool':,
#     #     }
#     #     json_data = json.dumps(data)
#     #     response = requests.post('{}/value/create_value'.format(host), data = json_data, headers = headers)
#     #     if response.status_code in [201, 409]:
#     #         pass
#     #     else:
#     #         print (response.status_code)
        
        
#     #     '''el_criteria_has_criterion'''
#     #     criterion_id = lookup_an_id('criterion', criterion_code)
#     #     eligibility_criteria_id = lookup_an_id('eligibility_criteria', study_version_id)
#     #     value_id = lookup_an_id('value', value_code)
#     #     data = {
#     #         'criterion_id': criterion_id,
#     #         'eligibility_criteria_id': eligibility_criteria_id,
#     #         'active': 0,
#     #         'value_id': value_id,
#     #     }
#     #     json_data = json.dumps(data)
#     #     response = requests.post('{}/el_criteria_has_criterion/create_el_criteria_has_criterion'.format(host), data = json_data, headers = headers)
#     #     if response.status_code in [201, 409]:
#     #         pass
#     #     else:
#     #         print (response.status_code)

        

    
    
# # if __name__ == '__main__':
# #     run()
