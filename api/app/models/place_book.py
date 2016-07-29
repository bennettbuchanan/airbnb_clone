'''Imports BaseModel, Place, and User classes and defines a PlaceBook class
that inherits from BaseModel class.
'''
from base import *
from peewee import *
from place import Place
from user import User
from datetime import datetime


class PlaceBook(BaseModel):
    place = ForeignKeyField(Place)
    user = ForeignKeyField(User, related_name='placesbooked')
    is_validated = BooleanField(default=False)
    date_start = DateTimeField(null=False)
    number_nights = IntegerField(default=1)

    def to_dict(self):
        '''Returns the BaseModel data, along with this model model's data as a
        hash.
        '''

        data = {}
        data['place_id'] = self.place.id
        data['user_id'] = self.user.id
        data['is_validated'] = self.is_validated

        '''This condition is necessary to handle cases where this method is
        being called or when the object is unicode or a string. It keeps the
        formatting consistent for both returned strings.
        '''
        if type(self.date_start) == unicode:
            data['date_start'] = (datetime
                                  .strptime(self.date_start,
                                            "%Y/%m/%d %H:%M:%S")
                                  .strftime("%Y/%m/%d %H:%M:%S"))
        else:
            data['date_start'] = self.date_start.strftime("%Y/%m/%d %H:%M:%S")
        data['number_nights'] = self.number_nights
        return dict(self.base_to_dict().items() + data.items())
