'''Imports BaseModel and State classes and defines a City class that inherits
from BaseModel class.
'''
from base import *
from state import State
from peewee import *


class City(BaseModel):
    '''Define a City class for the city table of the database. Has a
    foreign key from the state table.
    '''
    city = CharField(128, null=False)
    state = ForeignKeyField(State, related_name='cities', on_delete='CASCADE')

    def to_hash(self):
        '''Returns a hash of all the model's data.'''
        data = {}
        data['id'] = self.id
        data['created_at'] = self.created_at
        data['updated_at'] = self.updated_at
        data['name'] = self.name
        data['state_id'] = self.state.id
        json_data = json.dumps(data)
        return json_data
