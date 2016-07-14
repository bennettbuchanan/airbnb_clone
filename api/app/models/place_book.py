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
        '''Returns a hash of all the model's data.'''
        data = {}
        data['id'] = self.id
        data['created_at'] = self.created_at
        data['updated_at'] = self.updated_at
        data['place_id'] = self.place.id
        data['user_id'] = self.user.id
        data['is_validated'] = self.is_validated
        data['date_start'] = self.date_start
        data['number_nights'] = self.number_nights
        json_data = json.dumps(data)
        return json_data
