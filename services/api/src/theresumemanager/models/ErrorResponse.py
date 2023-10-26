import json

class ErrorResponse:
    def __init__(self, message, statusCode, status, data = {}):
        self.message = message
        self.statusCode = statusCode
        self.status = status
        self.data = data

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    def to_dict(self):
        return json.loads(self.to_json())
    
    def __str__(self):
        return self.to_json()