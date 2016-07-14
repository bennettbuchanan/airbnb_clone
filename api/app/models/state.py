'''Imports BaseModel and defines a State class that inherits from BaseModel
class.
'''
from base import *
from peewee import *
import json


class State(BaseModel):
    '''Define a State class for the state table of the database.'''
    name = CharField(128, null=False, unique=True)

    def to_hash(self):
        '''Returns a hash of all the model's data.'''
        data = {}
        data['id'] = self.id
        data['created_at'] = self.created_at
        data['updated_at'] = self.updated_at
        data['name'] = self.name
        json_data = json.dumps(data)
        return json_data
