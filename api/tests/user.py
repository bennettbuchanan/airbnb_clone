import unittest
import json
import logging
from app import app
from app.views import user
from app.models.user import User
from app.models.base import BaseModel
from peewee import *


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        '''Creates a test client, disables logging, connects to the database
        and creates a table User for temporary testing purposes.
        '''
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        BaseModel.database.connect()
        BaseModel.database.create_table(User)

    def tearDown(self):
        '''Drops the table User.'''
        BaseModel.database.drop_table(User)

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
        for i in range(1, 3):
            res = self.create_user("test", str(i), str(i), str(i))
            '''The dictionary returns an object with the correct id.'''
            self.assertEqual(json.loads(res.data).get("id"), i)

        lacking_param = self.app.post('/users', data=dict(first_name="test"))
        non_unique_email = self.create_user("test", str(i), str(i), str(i))

        self.assertEqual(lacking_param.status_code, 400)
        self.assertEqual(non_unique_email.status_code, 409)

    def test_list(self):
        res = self.app.get('/users')
        self.assertEqual(len(json.loads(res.data)), 0)

        '''Add one user to databse.'''
        self.create_user("test", "test", "test", "test")
        res = self.app.get('/users')
        self.assertEqual(len(json.loads(res.data)), 1)

    def test_get(self):
        res = self.create_user("user_1", "user_1", "user_1", "user_1")
        self.assertEqual(res.status_code, 201)

        res = self.app.get('/users/1')
        self.assertEqual(json.loads(res.data).get("first_name"), "user_1")

        '''The service returns 200 for a non existant user.'''
        res = self.app.get('/users/2')
        self.assertEqual(res.status_code, 404)

    def test_delete(self):
        '''Create a new user.'''
        res = self.create_user("user_1", "user_1", "user_1", "user_1")
        self.assertEqual(res.status_code, 201)

        '''Check that there is one user in the table.'''
        res = self.app.get('/users')
        self.assertEqual(len(json.loads(res.data)), 1)

        '''Delete the user and check that the table is empty.'''
        self.app.delete('/users/1')
        res = self.app.get('/users')
        self.assertEqual(len(json.loads(res.data)), 0)

        '''The service returns 404 when attempting to delete a non-existant
        user.
        '''
        res = self.app.delete('/users/1')
        self.assertEqual(res.status_code, 404)

    def test_update(self):
        '''Create a new user.'''
        res = self.create_user("user_1", "user_1", "user_1", "user_1")
        self.assertEqual(res.status_code, 201)

        '''Update user_1, check the status code.'''
        res = self.app.put('/users/1', data=dict(
            first_name="updated",
            last_name="updated",
        ))
        self.assertEqual(res.status_code, 201)
        res = self.app.get('/users')

        '''Check the values of the updated user are correct.'''
        keys = ["first_name", "last_name"]
        for key in keys:
            self.assertEqual(json.loads(res.data)[0].get(key), "updated")

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
