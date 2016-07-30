import unittest
import json
import logging
import time
from app import app
from app.views import *
from app.models.place import Place
from app.models.place_book import PlaceBook
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
        BaseModel.database.create_tables([User, City, Place, State, PlaceBook])

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

        '''Create two places.'''
        for i in range(1, 3):
            self.create_place('/places', 'test_' + str(i))

        '''Create a book on place 1, belonging to user 1.'''
        self.app.post('/places/1/books', data=dict(
            place=1,
            user=1,
            date_start="2000/1/1 00:00:00",
            description="test",
            number_nights=10,
            latitude=0,
            longitude=0
        ))

    def tearDown(self):
        '''Drops the state and city tables.'''
        BaseModel.database.drop_tables([User, City, Place, State, PlaceBook])

    def create_place(self, route, name_param):
        '''Makes a post request with the parameters in dict. This adds a city
        to the table City. These last three params are necessary to suppress
        warnings that there is no default value for the field.

        Keyword arguments:
        city_name -- The required name of the city.
        '''
        return self.app.post(route, data=dict(
            owner=1,
            city=1,
            name=name_param,
            description="test",
            latitude=0,
            longitude=0
        ))

    def test_create(self):
        '''The dictionary returns an object with the correct id.'''
        for i in range(3, 5):
            res = self.create_place('/places', 'test_' + str(i))
            self.assertEqual(json.loads(res.data)['id'], i)

    def test_create_id(self):
        '''The dictionary returns an object with the correct id.'''
        res = self.app.get('/places/2')
        self.assertEqual(json.loads(res.data)['id'], 2)

        '''Update the id of the item.'''
        self.app.put('/places/2', data=dict(name='updated_data'))
        res = self.app.get('/places/2')
        self.assertEqual(json.loads(res.data)['name'], 'updated_data')

        '''You may not update the owner.'''
        res = self.app.put('/places/1', data=dict(owner="test"))
        self.assertEqual(res.status_code, 409)

        '''You may not update the city.'''
        res = self.app.put('/places/1', data=dict(city="test"))
        self.assertEqual(res.status_code, 409)

    def test_delete(self):
        '''Delete place with the id 2.'''
        self.app.delete('/places/2')

        '''There is only one remaining place in the table, that with id 1.'''
        res = self.app.get('/places')
        self.assertEqual(len(json.loads(res.data)[0]['data']), 1)
        self.assertEqual(json.loads(res.data)[0]['data'][0]['id'], 1)

    def test_get_places_by_state(self):
        '''Test retrieval of places belonging to a state.'''
        res = self.app.get('/states/1/places')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.data)[0]['data']), 2)

        '''There is no state with this id. Return 400 status code.'''
        res = self.app.get('/states/2/places')
        self.assertEqual(res.status_code, 400)

    def test_get_places_by_id(self):
        '''Test creation of place in this city and state.'''
        res = self.app.get('/states/1/cities/1/places')
        self.assertEqual(len(json.loads(res.data)), 2)

        res = self.app.post('/states/1/cities/1/places', data=dict(
            owner=1,
            city=1,
            name="test",
            description="test",
            latitude=0,
            longitude=0
        ))

        res = self.app.get('/states/1/cities/1/places')
        self.assertEqual(len(json.loads(res.data)), 3)

    def test_get_place_availibility(self):
        '''Test the ability to query availability based on place bookings.'''
        res = self.app.get('/states/1/cities/1/places')
        self.assertEqual(len(json.loads(res.data)), 2)

        res = self.app.get('/places/1/books/1')

        res = self.app.post('/places/1/available', data=dict(year=2000,
                                                             month=1,
                                                             day=11))

        self.assertEqual(json.loads(res.data).get('available'), True)

        res = self.app.post('/places/1/available', data=dict(year=2000,
                                                             month=1,
                                                             day=1))

        res = self.app.post('/places/1/available', data=dict(year=2000,
                                                             month=1,
                                                             day=10))

        self.assertEqual(json.loads(res.data).get('available'), False)

        '''Add a new book for the 11th for one night. Test to see if availability
        is False.
        '''
        self.app.post('/places/1/books', data=dict(
            place=1,
            user=1,
            date_start="2000/1/11 00:00:00",
            description="test",
            number_nights=1,
            latitude=0,
            longitude=0
        ))

        res = self.app.post('/places/1/available', data=dict(year=2000,
                                                             month=1,
                                                             day=11))

        self.assertEqual(json.loads(res.data).get('available'), False)

        '''Test for missing parameter in POST request.'''
        missing_param = self.app.post('/places/1/available',
                                      data=dict(year=2000))

        self.assertEqual(missing_param.status_code, 400)

if __name__ == '__main__':
    unittest.main()
