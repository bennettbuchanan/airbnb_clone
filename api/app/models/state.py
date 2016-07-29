'''Imports BaseModel and defines a State class that inherits from BaseModel
class.
'''
from base import *
from peewee import *
import json


class State(BaseModel):
    '''Define a State class for the state table of the database.'''
    name = CharField(128, null=False, unique=True)

    def to_dict(self):
        '''Returns the BaseModel data, along with this model model's data as a
        hash.
        '''
        data = {}
        data['name'] = self.name
        return dict(self.base_to_dict().items() + data.items())
