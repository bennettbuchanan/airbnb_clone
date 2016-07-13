'''Imports BaseModel and defines an Amenity class that inherits from BaseModel
class.
'''
from base import *
from peewee import *


class Amenity(BaseModel):
    '''Defines an amenity class.'''
    name = CharField(128, null=False)
