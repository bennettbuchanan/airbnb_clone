'''Imports BaseModel and defines a State class that inherits from BaseModel
class.
'''
from base import *
from peewee import *


class State(BaseModel):
    '''Define a State class for the state table of the database.'''
    name = CharField(128, null=False, unique=True)
