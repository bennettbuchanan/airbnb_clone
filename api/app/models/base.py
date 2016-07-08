'''Sets MySQL variable database with all configuration settings from the right
config file depending on the environment.
'''
from peewee import *
import os
import json
import datetime
from .. import config


'''Fetch the database values and store them as a list.'''
env = os.environ.get('DATABASE')
env = json.loads(env)


'''Create the SQLite database based on appropriate ENV variables.'''
db = MySQLDatabase(env.get("database"),
                   host=env.get("host"),
                   port=env.get("port"),
                   user=env.get("user"),
                   passwd=env.get("password"))


class BaseModel(Model):
    '''A BaseModel class for other tables to inherit from.'''
    id = PrimaryKeyField(primary_key=True, unique=True)
    database = db
    created_at = DateTimeField(default=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    updated_at = DateTimeField(default=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    def save(self, *args, **kwargs):
        '''Overloading operator save that updates the current datetime before
        calling the parent save method.

        Keyword arguments:
        args -- A non-keyworded argument list.
        kwards -- A dict of keyword arguments passed to the function.
        '''
        self.updated_at = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    class Meta:
        '''Define the database from which this class is created.'''
        database = db
        order_by = ('id', )
