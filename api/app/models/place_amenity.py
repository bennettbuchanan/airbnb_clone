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
