from base import *
from peewee import *
import md5


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
