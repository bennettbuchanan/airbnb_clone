'''Imports Model and defines a ReviewUser class that inherits from it.'''
from base import *
from peewee import *
from user import User
from review import Review


class ReviewUser(Model):
    user = ForeignKeyField(User)
    review = ForeignKeyField(Review)

    class Meta:
        '''Define the database from which this class is created. In this case,
        the same database that is used for BaseModel.'''
        database = db
