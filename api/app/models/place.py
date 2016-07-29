'''Imports BaseModel, User, and City classes and defines a Place class that
inherits from BaseModel class.
'''
from base import *
from peewee import *
from user import User
from city import City


class Place(BaseModel):
    '''Define a Place class for the city table of the database.'''
    owner = ForeignKeyField(User, related_name='places')
    city = ForeignKeyField(City, related_name='places')
    name = CharField(128, null=False)
    description = TextField()
    number_rooms = IntegerField(default=0)
    number_bathrooms = IntegerField(default=0)
    max_guest = IntegerField(default=0)
    price_by_night = IntegerField(default=0)
    latitude = FloatField()
    longitude = FloatField()

    def to_dict(self):
        '''Returns the BaseModel data, along with this model model's data as a
        hash.
        '''
        data = {}
        data['owner_id'] = self.owner.id
        data['city_id'] = self.city.id
        data['name'] = self.name
        data['description'] = self.description
        data['number_rooms'] = self.number_rooms
        data['number_bathrooms'] = self.number_bathrooms
        data['max_guest'] = self.max_guest
        data['price_by_night'] = self.price_by_night
        data['latitude'] = self.latitude
        data['longitude'] = self.longitude
        return dict(self.base_to_dict().items() + data.items())
