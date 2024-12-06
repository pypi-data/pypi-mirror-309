import json


def JSONReadable(data):
    if type(data) != dict:
        data = json.loads(data)
    return json.dumps(data, indent=4, sort_keys=True)
