'''Imports BaseModel and defines an Amenity class that inherits from BaseModel
class.
'''
from base import *
from peewee import *


class Amenity(BaseModel):
    '''Defines an amenity class.'''
    name = CharField(128, null=False)

    def to_dict(self):
        '''Returns the BaseModel data, along with this model model's data as a
        hash.
        '''
        data = {}
        data['name'] = self.name
        return dict(self.base_to_dict().items() + data.items())
