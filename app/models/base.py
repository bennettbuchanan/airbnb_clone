'''Sets MySQL variable database with all configuration settings from the right
config file depending on the environment.
'''

from peewee import *
import os
from .. import config

# host = ../../api/config.py
# port
# user
# passwd
#
# '''Create the SQLite database based on appropriate ENV variables.'''
# db = peewee.MySQLDatabase("mydb",
#                           host="mydb.crhauek3cxfw.us-west-2.rds.amazonaws.com",
#                           port=3306,
#                           user="user",
#                           passwd="password")
#
#
# class BaseModel(peewee.Model):
#     '''Define a BaseModel class for other tables to derive from.'''
#     id = PrimaryKeyField(primary_key=True, unique=True)
#     database = db
#
#     class Meta:
#         '''Define the database from which this class is created.'''
#         database = my_models_db
#         order_by = ('id', )

print(os.environ["HOST"])
