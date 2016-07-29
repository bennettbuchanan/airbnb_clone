'''Imports BaseModel and defines a Review class that inherits from BaseModel
class.
'''
from base import *
from peewee import *
from user import User
from flask import jsonify
import json


class Review(BaseModel):
    '''Define a User class for the user table of the database.'''
    message = TextField(null=False)
    stars = IntegerField(default=0)
    user = ForeignKeyField(User, related_name="reviews", on_delete='CASCADE')

    def to_dict(self):
        '''Returns the BaseModel data, along with this model model's data as a
        hash. Circular imports need to be within the method scope. Query the
        tables to return the id of the user or place for which the review is
        of.
        '''
        from review_user import ReviewUser
        from review_place import ReviewPlace

        data = dict(message=self.message, stars=self.stars,
                    user=self.user.id, fromuserid=self.user.id)

        try:
            review = (ReviewUser
                      .select()
                      .where(ReviewUser.review == self.id)
                      .get())
            data['touserid'] = review.user.id
        except ReviewUser.DoesNotExist:
            data['touserid'] = None

        try:
            review = (ReviewPlace
                      .select()
                      .where(ReviewPlace.review == self.id)
                      .get())
            data['toplaceid'] = review.place.id
        except ReviewPlace.DoesNotExist:
            data['toplaceid'] = None

        return dict(self.base_to_dict().items() + data.items())
