import unittest
import json
import logging
from app import app
from app.views import *
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from app.models.place import Place
from app.models.user import User
from app.models.state import State
from app.models.city import City
from app.models.base import BaseModel
from peewee import *
from datetime import datetime


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        '''Creates a test client, disables logging, connects to the database
        and creates state and city tables for temporary testing purposes.
        '''
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        BaseModel.database.connect()
        BaseModel.database.create_tables([User, City, Place, State, Amenity,
                                          PlaceAmenities])

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

        self.app.post('/places', data=dict(
            owner=1,
            city=1,
            name="test",
            description="test",
            latitude=0,
            longitude=0
        ))

    def tearDown(self):
        '''Drops the state and city tables.'''
        BaseModel.database.drop_tables([User, City, Place, State, Amenity,
                                        PlaceAmenities])

    def create_amenity(self, route, amenity_name):
        '''Makes a post request with the parameters in dict. This adds an
        amenity to the table Amenity.

        Keyword arguments:
        route -- The route of the request.
        amenity_name -- The name of the new amenity.
        '''
        return self.app.post(route, data=dict(
            name=amenity_name
        ))

    def test_create(self):
        for i in range(1, 3):
            res = self.create_amenity('/amenities', 'test_' + str(i))

            '''The dictionary returns an object with the correct id.'''
            self.assertEqual(json.loads(res.data).get('id'), i)

        res = self.app.get('/amenities')
        self.assertEqual(len(json.loads(res.data)), 2)

        res = self.create_amenity('/amenities', "test_2")

        '''Do not allow a user to update the name.'''
        self.assertEqual(res.status_code, 409)
        self.assertEqual(json.loads(res.data).get('code'), 10003)

    def test_get_id(self):
        for i in range(1, 3):
            res = self.create_amenity('/amenities', 'test_' + str(i))

        res = self.app.get('/amenities/2')
        self.assertEqual(json.loads(res.data).get("id"), 2)

    def test_delete(self):
        for i in range(1, 3):
            res = self.create_amenity('/amenities', 'test_' + str(i))

        '''Delete amenity with the id 1.'''
        self.app.delete('/amenities/1')

        '''There is only one remaining booking in the table, that with id 2.'''
        res = self.app.get('/amenities')
        self.assertEqual(len(json.loads(res.data)), 1)
        self.assertEqual(json.loads(res.data)[0].get('id'), 2)

    def test_amenity_create_and_delete(self):
        '''Add a new amenity.'''
        for i in range(1, 3):
            res = self.create_amenity('/amenities', 'place_amenity_' + str(i))

        '''Add the amenity with id 1 to belong to place with id of 1. Test that
        it can be retrieved with a GET request on the same place's id.'''
        res = self.app.post('/places/1/amenities/1')
        res = self.app.post('/places/1/amenities/2')
        self.assertEqual(res.status_code, 201)
        res = self.app.get('/places/1/amenities')
        self.assertEqual(json.loads(res.data)[0].get('name'),
                         'place_amenity_1')
        self.assertEqual(len(json.loads(res.data)), 2)

        '''A POST request of a non existant amenity or place returns 404
        status.'''
        res = self.app.post('/places/1/amenities/3')
        self.assertEqual(res.status_code, 404)
        res = self.app.post('/places/2/amenities/1')
        self.assertEqual(res.status_code, 404)

        '''Delete amenity with id 1. There should be only one amenity for this
        place returned now.'''
        res = self.app.delete('/places/1/amenities/1')
        self.assertEqual(res.status_code, 200)
        res = self.app.get('/places/1/amenities')
        self.assertEqual(json.loads(res.data)[0].get('name'),
                         'place_amenity_2')
        self.assertEqual(len(json.loads(res.data)), 1)

if __name__ == '__main__':
    unittest.main()
