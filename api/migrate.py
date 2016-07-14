'''Import peewee models from their respective folders and create the tables in
the database. In addition to accessing BaseModel class, the importing of base
is required moreover for base.py to access the variables set up in config.py.
'''
from app.models.user import User
from app.models.state import State
from app.models.city import City
from app.models.place import Place
from app.models.place_book import PlaceBook
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from app.models.base import BaseModel
from peewee import *

tables = [User,
          State,
          City,
          Place,
          PlaceBook,
          Amenity,
          PlaceAmenities]

BaseModel.database.connect()
BaseModel.database.create_tables(tables)
