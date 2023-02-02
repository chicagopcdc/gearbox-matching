import json

def json_extract_ints(obj, key):

    arr = set()

    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, int):
                    arr.add(item)       
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return list(values)
