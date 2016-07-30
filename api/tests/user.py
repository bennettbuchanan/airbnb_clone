import unittest
import json
import logging
from app import app
from app.views import user
from app.models.user import User
from app.models.base import BaseModel
from peewee import *
import time
from datetime import datetime


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        '''Creates a test client, disables logging, connects to the database
        and creates a table User for temporary testing purposes.
        '''
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        BaseModel.database.connect()
        BaseModel.database.create_tables([User])

    def tearDown(self):
        '''Drops the table User.'''
        BaseModel.database.drop_tables([User])

    def create_user(self, first, last, address, pw):
        '''Makes a post request with the parameters in dict. Essentially this
        adds a user to the table User.

        Keyword arguments:
        first -- The required first name of the user.
        **op -- An optional argument (e.g., "pw") for testing purposes.
        '''
        return self.app.post('/users', data=dict(
            first_name=first,
            last_name=last,
            email=address,
            password=pw
        ))

    def test_create(self):
        '''The dictionary returns an object with the correct id.'''
        for i in range(1, 3):
            res = self.create_user("test", str(i), str(i), str(i))
            self.assertEqual(json.loads(res.data)['id'], i)

        lacking_param = self.app.post('/users', data=dict(first_name="test"))
        non_unique_email = self.create_user("test", str(i), str(i), str(i))
        self.assertEqual(lacking_param.status_code, 400)
        self.assertEqual(non_unique_email.status_code, 409)

    def test_list(self):
        '''Add one user to databse.'''
        res = self.app.get('/users')
        self.assertEqual(len(json.loads(res.data)[0]['data']), 0)

        for i in range(1, 16):
            self.create_user("test_" + str(i), "test_" + str(i),
                             "test_" + str(i), "test_" + str(i))

        '''Default returns 10 items.'''
        res = self.app.get('/users')
        self.assertEqual(len(json.loads(res.data)[0]['data']), 10)

        res = self.app.get('/users?page=2&number=10')
        self.assertEqual(len(json.loads(res.data)[0]['data']), 5)
        self.assertEqual(
            json.loads(res.data)[1]['paging']['next'], None)

        res = self.app.get('/users?page=1&number=10')
        self.assertEqual(len(json.loads(res.data)[0]['data']), 10)
        self.assertEqual(
            json.loads(res.data)[1]['paging']['previous'], None)

        res = self.app.get('/users?page=2&number=2')
        self.assertNotEqual(
            json.loads(res.data)[1]['paging']['next'], None)
        self.assertNotEqual(
            json.loads(res.data)[1]['paging']['previous'], None)

    def test_get(self):
        '''The service returns gets the proper user when id is passed in the
        URL path, and returns a 200 status_code for a non existant user.'''
        res = self.create_user("user_1", "user_1", "user_1", "user_1")
        self.assertEqual(res.status_code, 201)

        res = self.app.get('/users/1')
        self.assertEqual(json.loads(res.data)['first_name'], "user_1")

        res = self.app.get('/users/2')
        self.assertEqual(res.status_code, 404)

    def test_delete(self):
        '''Create a new user. Confirm 201 status code.'''
        res = self.create_user("user_1", "user_1", "user_1", "user_1")
        self.assertEqual(res.status_code, 201)

        '''Check that there is one user in the table.'''
        res = self.app.get('/users')
        self.assertEqual(len(json.loads(res.data)[0]['data']), 1)

        '''Delete the user and check that the table is empty.'''
        self.app.delete('/users/1')
        res = self.app.get('/users')
        self.assertEqual(len(json.loads(res.data)[0]['data']), 0)

        '''The service returns 404 when attempting to delete a non-existant
        user.
        '''
        res = self.app.delete('/users/1')
        self.assertEqual(res.status_code, 404)

    def test_update(self):
        '''Create a new user.'''
        res = self.create_user("user_1", "user_1", "user_1", "user_1")
        self.assertEqual(res.status_code, 201)

        '''Delay 2 seconds so `updated_at` value will be different than
        `created_at`.'''
        time.sleep(2)

        '''Update user_1, check the status code.'''
        res = self.app.put('/users/1', data=dict(
            first_name="updated",
            last_name="updated",
            created_at="1989/07/10 22:00:00",
            updated_at="1989/07/10 22:00:00"
        ))

        self.assertEqual(res.status_code, 201)
        res = self.app.get('/users')

        '''PUT request may not update created_at or updated_at fields.'''
        self.assertNotEqual(json.loads(res.data)[0]['data'][0]['updated_at'],
                            "1989/07/10 22:00:00")
        self.assertNotEqual(json.loads(res.data)[0]['data'][0]['created_at'],
                            "1989/07/10 22:00:00")

        '''`updated_at` value should be ahead of `created_at` by at least
        2 seconds.'''
        self.assertNotEqual(json.loads(res.data)[0]['data'][0]['created_at'],
                            json.loads(res.data)[0]['data'][0]['updated_at'])

        '''Check the values of the updated user are correct.'''
        keys = ["first_name", "last_name"]
        for key in keys:
            self.assertEqual(json.loads(res.data)[0]['data'][0][key],
                             "updated")

        '''The service returns 404 when attempting to update a non-existant
        user.'''
        res = self.app.put('/users/2', data=dict(
            first_name="updated",
            last_name="updated",
        ))
        self.assertEqual(res.status_code, 404)

        '''The service returns 409 when attempting to update a user's email
        because updating the email will result in a conflict.'''
        res = self.app.put('/users/1', data=dict(
            email="updated"
        ))
        self.assertEqual(res.status_code, 409)

if __name__ == '__main__':
    unittest.main()
