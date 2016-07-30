import unittest
import json
import logging
from app import app
from app.views import state
from app.models.state import State
from app.models.base import BaseModel
from peewee import *


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        '''Creates a test client, disables logging, connects to the database
        and creates a table State for temporary testing purposes.
        '''
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        BaseModel.database.connect()
        BaseModel.database.create_tables([State])

    def tearDown(self):
        '''Drops the table State.'''
        BaseModel.database.drop_tables([State])

    def create_state(self, state_name):
        '''Makes a post request with the parameters in dict. This adds a state
        to the table State.

        Keyword arguments:
        state_name -- The required name of the state.
        '''
        return self.app.post('/states', data=dict(
            name=state_name
        ))

    def test_create(self):
        '''The dictionary returns an object with the correct id.'''
        for i in range(1, 3):
            res = self.create_state("test_" + str(i))
            self.assertEqual(json.loads(res.data)['id'], i)

        lacking_param = self.app.post('/states', data=dict(bad_param="test"))
        non_unique_name = self.create_state("test_2")

        self.assertEqual(lacking_param.status_code, 400)
        self.assertEqual(non_unique_name.status_code, 409)

    def test_list(self):
        res = self.app.get('/states')
        self.assertEqual(len(json.loads(res.data)[0]['data']), 0)

        '''Add one state to databse.'''
        self.create_state("test")
        res = self.app.get('/states')
        self.assertEqual(len(json.loads(res.data)[0]['data']), 1)

    def test_delete(self):
        '''Create a new state, confirm 201 status code.'''
        res = self.create_state("test")
        self.assertEqual(res.status_code, 201)

        '''Check that there is one state in the table.'''
        res = self.app.get('/states')
        self.assertEqual(len(json.loads(res.data)[0]['data']), 1)

        '''Delete the state and check that the table is empty.'''
        self.app.delete('/states/1')
        res = self.app.get('/states')
        self.assertEqual(len(json.loads(res.data)[0]['data']), 0)

        '''The service returns 404 when attempting to delete a non-existant
        state.
        '''
        res = self.app.delete('/states/1')
        self.assertEqual(res.status_code, 404)

if __name__ == '__main__':
    unittest.main()
