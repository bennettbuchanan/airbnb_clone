'''Imports BaseModel, Place, and User classes and defines a PlaceBook class
that inherits from BaseModel class.
'''
from base import *
from peewee import *
from place import Place
from user import User


class PlaceBook(BaseModel):
    place = ForeignKeyField(Place)
    user = ForeignKeyField(User, related_name='placesbooked')
    is_validated = BooleanField(default=False)
    date_start = DateTimeField(null=False)
    number_nights = IntegerField(default=1)

    def to_hash(self):
        '''Returns the BaseModel data, along with this model model's data as a
        hash.
        '''
        data = {}
        data['place_id'] = self.place.id
        data['user_id'] = self.user.id
        data['is_validated'] = self.is_validated
        data['date_start'] = self.date_start
        data['number_nights'] = self.number_nights
        return dict(self.base_to_hash().items() + data.items())
