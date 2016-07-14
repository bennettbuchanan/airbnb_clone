'''Imports BaseModel and defines an Amenity class that inherits from BaseModel
class.
'''
from base import *
from peewee import *


class Amenity(BaseModel):
    '''Defines an amenity class.'''
    name = CharField(128, null=False)

    def to_hash(self):
        '''Returns a hash of all the model's data.'''
        data = {}
        data['id'] = self.id
        data['created_at'] = self.created_at
        data['updated_at'] = self.updated_at
        data['name'] = self.name
        json_data = json.dumps(data)
        return json_data
