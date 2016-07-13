'''Imports db variable (the database to connect to on the server), Place, and
Amenity classes and defines a PlaceAmenities class that inherits from the
peewee Model class. For more information regarding the peewee Model see:
http://docs.peewee-orm.com/en/latest/peewee/models.html.
'''
from base import *
from peewee import *
from place import Place
from amenity import Amenity


class PlaceAmenities(Model):
    place = ForeignKeyField(Place)
    amenity = ForeignKeyField(Amenity)

    class Meta:
        '''Define the database from which this class is created. In this case,
        the same database that is used for BaseModel.'''
        database = db
