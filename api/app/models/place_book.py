'''Imports BaseModel, Place, and User classes and defines a PlaceBook class
that inherits from BaseModel class.
'''
from base import *
from peewee import *
from place import Place
from user import User


class PlaceBook(BaseModel):
    place = ForeignKeyField(Place)
    user = ForeignKeyField(User, related_name='placesbooked')
    is_validated = BooleanField(default=False)
    date_start = DateTimeField(null=False)
    number_nights = IntegerField(default=1)
