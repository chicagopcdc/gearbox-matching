import json

import numpy as np
import pandas as pd
import requests

############################

data_path = '~/Desktop/tables/'
data_prefix = 'v18/load_trials_v18 - '
host = 'http://0.0.0.0:5000'
headers = {'Content-type': 'application/json'}

############################

def create(table, ignore):
    print (table)
    filename = data_path + data_prefix + table + '.csv'
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

        #print(json_payload)
        
        response = requests.post('{}/{}/create_{}'.format(host, table, table), data = json_payload, headers = headers)
        if response.status_code in [201, 409]:
            print ('success: {}'.format(response.status_code))
        else:
            print ("-------------------->> FAILfailFAILfailFAIL: {}".format(response.status_code))
            print (json_payload)
    print ('\n\n')

########################################################


# create('study', ['id', 'create_date'])
# create('study_version', ['id', 'create_date'])
# create('value', ['id'])
# create('input_type', ['id'])
# create('tag', ['id'])
# create('criterion', ['id'])
# create('criterion_has_value', ['create_date'])
# create('eligibility_criteria', ['id', 'create_date'])

# create('display_rules', ['id', 'active', 'version'])

create('triggered_by', ['id', 'active'])

#create('criterion_has_tag', None)

#create('el_criteria_has_criterion', ['id'])

#create('algorithm_engine', ['id'])

#create('study_algorithm_engine', None)
