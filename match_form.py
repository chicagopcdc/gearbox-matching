import json
import copy

import pandas as pd

################################

def is_active(row):
    if exactly_1(row):
        try:
            if pd.isna(row.active):
                return True #assume null = active
            else:
                return bool(pd.eval(row.active))
        except:
            if pd.isna(row.active.values[0]): #sometimes need .values[0] to get a number
                return True #assume null = active
            else:
                return bool(pd.eval(row.active))            
    else:
        print ("is_active() cannot operate on multiple rows\n")
        return False
        
def exactly_1(found):
    n = found.shape[0]
    if n==1 or len(found.shape)==1:
        return True
    else:
        return False

def n_rows(found):
    return found.shape[0]


def triggers(row, triggered_by, value):
    display_rules_id = row.id
    tbs = triggered_by.loc[triggered_by.display_rules_id==display_rules_id]
    if len(tbs.values)>0:
        for index, tb in tbs.iterrows(): #can be triggered by more than one crit/val combo
            if is_active(tb):
                criterion_id = int(tb.criterion_id)

                #get val and operator
                value_id = int(tb.value_id)
                val = value.loc[value.id==value_id]                           

                if exactly_1(val) and is_active(val):
                    operator = val.operator.values[0]
                    the_value = val.value_string.values[0]
                else:
                    return {}
                
                path = tb.path

                if not pd.isna(path):
                    crits = showIf.get('criteria')
                    new_crit = {
                                'id': criterion_id,
                                'operator': operator,
                                'value': eval(the_value)
                            }
                    crits.append(new_crit)
                    showIf.update({'criteria': crits})
                else: #no path, just one crit
                    showIf = {
                        'operator': 'OR',
                        'criteria': [
                            {
                                'id': criterion_id,
                                'operator': operator,
                                'value': eval(the_value)
                            }
                        ]
                    }
                    
        return showIf
    else:
        return {}


##################################

data_path = '~/Desktop/tables/'
data_prefix = 'v20/load_trials_v20 - '

tables = [
    'study',
    'study_version',
    'value',
    'input_type',
    'tag',
    'criterion',
    'criterion_has_value',
    'eligibility_criteria',
    'display_rules',
    'triggered_by',
    'criterion_has_tag'
]

DF = {}
for table in tables:
    filename = data_path + data_prefix + table + '.csv'
    df = pd.read_csv(filename)
    DF.update({table: df})

tag = DF['tag']
criterion_has_tag = DF['criterion_has_tag']
criterion_has_value = DF['criterion_has_value']
value = DF['value']
triggered_by = DF['triggered_by']
input_type = DF['input_type']
criterion = DF['criterion']
display_rules = DF['display_rules']


# #REQUIRED
#'id', #unique id for the field
#'groupId', #one of the IDs in "groups"
#'name', #field name
#'type', #one of the following: "checkbox", "radio", "number", "text", "select", "multiselect", "age"
##OPTIONAL
#'label', #label text to display; avilable for all field types
#'showIf', #for conditional display; available for all field types    
#'options', #options to choose from; available for field types "radio", "select", "multiselect"
#'placeholder', #placeholder text to display; available for field types "number", "text", "select", "multiselect"


#sort by priority
df = display_rules.sort_values(by=['priority'])

#DEBUG
df = df.head(9)

G = []
for idx, row in tag.iterrows():
    g = {
        'id': row.id,
        'name': row.code
    }
    G.append(g)

F = []
for i in range(0, len(df)):
    print ("\n\ni = {}".format(i))
    row = df.iloc[i]

    #if row is not active, do nothing
    if is_active(row):
        criterion_id = int(row.criterion_id)

        #1 of the 4 required
        f = {'id': criterion_id}

        cht = criterion_has_tag.loc[criterion_has_tag.criterion_id==criterion_id]
        tag_id = int(cht.tag_id) #.values[0])
        #2 of the 4 required
        f.update({'groupId': tag_id})
        
        crit = criterion.loc[criterion.id==criterion_id]

        if exactly_1(crit): #should always be true
            if is_active(crit):
                #set the name
                #3 of 4 required
                f.update({'name':  crit.code.values[0]})
                #set the label
                f.update({'label': crit.display_name.values[0]})
                    
                #prep to set the type
                input_type_id = crit.input_type_id.values[0]
                it = input_type.loc[input_type.id==input_type_id]
                
                if exactly_1(crit):
                    #set the type
                    #4 of 4 required
                    f.update({'type': it.render_type.values[0]})


                #convert any into showIf statement
                showIf = triggers(row, triggered_by, value)
                if showIf:
                    f.update({'showIf': showIf})

                #see if muliple values
                chv = criterion_has_value.loc[criterion_has_value.criterion_id==criterion_id]
                if n_rows(chv) in [0, 1]:
                    pass
                else: #criterion has multiple vals
                    f.update({'placeholder': 'Select'})

                    options = []
                    vals = list(chv.value_id.values)
                    for val in vals:
                        o = {'value': val}

                        v_row = value.loc[value.id==val]
                        o.update({'label': v_row.code.values[0]})

                        #description not used anymore?
                        o.update({'description': v_row.description.values[0]})

                        options.append(o)

                    f.update({'options': options})
    F.append(f)