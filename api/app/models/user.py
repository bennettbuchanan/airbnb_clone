'''Imports BaseModel and defines a User class that inherits from BaseModel
class.
'''
from base import *
from peewee import *
import md5
from flask import jsonify
import json


class User(BaseModel):
    '''Define a User class for the user table of the database.'''
    email = CharField(128, null=False, unique=True)
    password = CharField(128, null=False)
    first_name = CharField(128, null=False)
    last_name = CharField(128, null=False)
    is_admin = BooleanField(default=False)

    def set_password(self, clear_password):
        '''Method to convert password passed as parameter to md5 hash and
        update the user's password to the hashed string.

        Keyword arguments:
        clear_password -- A new password string.
        '''
        self.password = md5.new(clear_password).digest()

    def to_dict(self):
        '''Returns the BaseModel data, along with this model model's data as a
        hash.
        '''
        data = {}
        data['email'] = self.email
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        return dict(self.base_to_dict().items() + data.items())
