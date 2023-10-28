from .operations.create import create_data
from .operations.read import read_data
from .operations.update import update_data, update_status_data
from .operations.delete import delete_data

def dummy_func(*kwargs):
    pass

class DB:
    def create(self, data, callback):
        create_data(data, callback)

    def read(self, uuid, callback=dummy_func):
        return read_data(uuid, callback)

    def read_all(self, callback):
        read_data(callback)

    def update(self, data, callback):
        update_data(data, callback)
    
    def update_status(self, uuid, status, callback, notes=""):
        update_status_data(uuid, status, notes, callback)

    def delete(self, uuid, callback):
        delete_data(uuid, callback)