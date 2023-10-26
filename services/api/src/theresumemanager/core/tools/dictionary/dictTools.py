import json

class obj:
    # constructor
    def __init__(self, dict):
        self.__dict__.update(dict)

def dict2obj(dict):
     
    # using json.loads method and passing json.dumps
    # method and custom object hook as arguments
    return json.loads(json.dumps(dict), object_hook=obj)