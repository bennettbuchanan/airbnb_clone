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
    '''update email field to , unique=True'''
    email = CharField(128, null=False)
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

    def to_hash(self):
        '''Returns a hash of all the model's data.'''
        data = {}
        data['id'] = self.id
        data['created_at'] = self.created_at
        data['updated_at'] = self.updated_at
        data['email'] = self.email
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        data['is_admin'] = self.is_admin
        json_data = json.dumps(data, sort_keys=True,
                               indent=4, separators=(',', ': '))
        return json_data
