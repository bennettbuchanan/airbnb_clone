import unittest
import json
import logging
from app import app
from app.views import *
from app.models.place import Place
from app.models.user import User
from app.models.state import State
from app.models.city import City
from app.models.base import BaseModel
from peewee import *


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        '''Creates a test client, disables logging, connects to the database
        and creates state and city tables for temporary testing purposes.
        '''
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        BaseModel.database.connect()
        BaseModel.database.create_tables([User, City, Place, State])

        '''Create items in tables for ForeignKeyField requirements'''
        self.app.post('/states', data=dict(name="test"))
        self.app.post('/states/1/cities', data=dict(
            name="test",
            state=1
        ))
        self.app.post('/users', data=dict(
            first_name="test",
            last_name="test",
            email="test",
            password="test"
        ))

    def tearDown(self):
        '''Drops the state and city tables.'''
        BaseModel.database.drop_tables([User, City, Place, State])

    def create_place(self, name_param):
        '''Makes a post request with the parameters in dict. This adds a city
        to the table City. These last three params are necessary to suppress
        warnings that there is no default value for the field.

        Keyword arguments:
        city_name -- The required name of the city.
        '''
        return self.app.post('/places', data=dict(
            owner=1,
            city=1,
            name=name_param,
            description="test",
            latitude=0,
            longitude=0
        ))

    def test_create(self):
        for i in range(1, 3):
            res = self.create_place("test_" + str(i))

            '''The dictionary returns an object with the correct id.'''
            self.assertEqual(json.loads(res.data).get("id"), i)

if __name__ == '__main__':
    unittest.main()
