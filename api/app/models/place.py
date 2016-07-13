'''Imports BaseModel, User, and City classes and defines a Place class that
inherits from BaseModel class.
'''
from base import *
from peewee import *
from user import User
from city import City


class Place(BaseModel):
    '''Define a Place class for the city table of the database.'''
    owner = ForeignKeyField(User, related_name='places')
    city = ForeignKeyField(City, related_name='places')
    name = CharField(128, null=False)
    description = TextField()
    number_rooms = IntegerField(default=0)
    number_bathrooms = IntegerField(default=0)
    max_guest = IntegerField(default=0)
    price_by_night = IntegerField(default=0)
    latitude = FloatField()
    longitude = FloatField()
