import unittest
import json
import logging
from app import app
from app.views import *
from app.models.user import User
from app.models.review import Review
from app.models.review_user import ReviewUser
from app.models.place import Place
from app.models.review_place import ReviewPlace
from app.models.city import City
from app.models.state import State
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
        BaseModel.database.create_tables([User, Place, Review, ReviewPlace,
                                          ReviewUser, City, State])

        '''Add two new users.'''
        for i in range(1, 3):
            self.app.post('/users', data=dict(first_name="user_" + str(i),
                                              last_name="user_" + str(i),
                                              email="user_" + str(i),
                                              password="user_" + str(i)))

        '''Add a state.'''
        self.app.post('/states', data=dict(name="state_1"))

        '''Add a city.'''
        self.app.post('/states/1/cities', data=dict(name="city_1", state=1))

        '''Add a place.'''
        self.app.post('/places', data=dict(owner=1, city=1, name="place_1",
                                           description="place_1", latitude=0,
                                           longitude=0))

    def tearDown(self):
        '''Drops the table User.'''
        BaseModel.database.drop_tables([User, Place, Review, ReviewPlace,
                                        ReviewUser, City, State])

    def create_review(self, route, message_str):
        '''Makes a post request with the parameters in dict. Essentially this
        adds a user to the table User.

        Keyword arguments:
        first -- The required first name of the user.
        **op -- An optional argument (e.g., "pw") for testing purposes.
        '''
        return self.app.post(route, data=dict(
            message=message_str,
            user=1
        ))

    def test_create(self):
        for i in range(1, 3):
            res = self.create_review('/users/2/my_reviews', 'test_' + str(i))

            '''The dictionary returns an object with the correct id.'''
            self.assertEqual(json.loads(res.data).get("id"), i)

            '''The dictionary returns an object with userid that corresponds
            to the user id in the route. In this case, 2.
            '''
            self.assertEqual(json.loads(res.data).get("fromuserid"), 2)


    # def test_list(self):
    #     res = self.app.get('/users')
    #     self.assertEqual(len(json.loads(res.data)), 0)
    #
    #     '''Add one user to databse.'''
    #     self.create_user("test", "test", "test", "test")
    #     res = self.app.get('/users')
    #     self.assertEqual(len(json.loads(res.data)), 1)
    #
    # def test_get(self):
    #     res = self.create_user("user_1", "user_1", "user_1", "user_1")
    #     self.assertEqual(res.status_code, 201)
    #
    #     res = self.app.get('/users/1')
    #     self.assertEqual(json.loads(res.data).get("first_name"), "user_1")
    #
    #     '''The service returns 200 for a non existant user.'''
    #     res = self.app.get('/users/2')
    #     self.assertEqual(res.status_code, 404)
    #
    # def test_delete(self):
    #     '''Create a new user. Confirm 201 status code.'''
    #     res = self.create_user("user_1", "user_1", "user_1", "user_1")
    #     self.assertEqual(res.status_code, 201)
    #
    #     '''Check that there is one user in the table.'''
    #     res = self.app.get('/users')
    #     self.assertEqual(len(json.loads(res.data)), 1)
    #
    #     '''Delete the user and check that the table is empty.'''
    #     self.app.delete('/users/1')
    #     res = self.app.get('/users')
    #     self.assertEqual(len(json.loads(res.data)), 0)
    #
    #     '''The service returns 404 when attempting to delete a non-existant
    #     user.
    #     '''
    #     res = self.app.delete('/users/1')
    #     self.assertEqual(res.status_code, 404)
    #
    # def test_update(self):
    #     '''Create a new user.'''
    #     res = self.create_user("user_1", "user_1", "user_1", "user_1")
    #     self.assertEqual(res.status_code, 201)
    #
    #     '''Update user_1, check the status code.'''
    #     res = self.app.put('/users/1', data=dict(
    #         first_name="updated",
    #         last_name="updated",
    #     ))
    #     self.assertEqual(res.status_code, 201)
    #     res = self.app.get('/users')
    #
    #     '''Check the values of the updated user are correct.'''
    #     keys = ["first_name", "last_name"]
    #     for key in keys:
    #         self.assertEqual(json.loads(res.data)[0].get(key), "updated")
    #
    #     '''The service returns 404 when attempting to update a non-existant
    #     user.'''
    #     res = self.app.put('/users/2', data=dict(
    #         first_name="updated",
    #         last_name="updated",
    #     ))
    #     self.assertEqual(res.status_code, 404)
    #
    #     '''The service returns 409 when attempting to update a user's email
    #     because updating the email will result in a conflict.'''
    #     res = self.app.put('/users/1', data=dict(
    #         email="updated"
    #     ))
    #     self.assertEqual(res.status_code, 409)

if __name__ == '__main__':
    unittest.main()
