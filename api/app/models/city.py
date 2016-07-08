class City(BaseModel):
    '''Define a City class for the city table of the database. Has a
    foreign key from the state table.
    '''
    city = CharField(128, null=False)
    state = ForeignKeyField(State, related_name='cities', on_delete='CASCADE')
