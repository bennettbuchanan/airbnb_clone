'''Imports Model and defines a ReviewPlace class that inherits from it.'''
from base import *
from peewee import *
from place import Place
from review import Review


class ReviewPlace(Model):
    place = ForeignKeyField(Place)
    review = ForeignKeyField(Review)

    class Meta:
        '''Define the database from which this class is created. In this case,
        the same database that is used for BaseModel.'''
        database = db
