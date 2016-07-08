from base import *
from peewee import *


class Amenity(BaseModel):
    name = CharField(128, null=False)
