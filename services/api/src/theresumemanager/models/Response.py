import json

class Response:
    def __init__(self, status, statusCode, message, data = {}):
        self.status = status
        self.statusCode = statusCode
        self.message = message
        self.data = data

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    def to_dict(self):
        return json.loads(self.to_json())

    def __str__(self):
        return self.to_json()