from flask import request, jsonify
from datetime import datetime, timedelta
from app.models.place import Place
from app.models.place_book import PlaceBook
from app.models.state import State
from app.models.city import City
from return_styles import ListStyle
from app import app


@app.route('/places', methods=['GET', 'POST'])
def handle_places():
    '''Returns all the places with a GET request, or adds a new city to the
    database with a POST request. The parameters passed to the POST request
    iterate through the data and set the corresponding attributes of the
    instance to  be inserted into the database. Will not set attribute passed
    as `updated_at` or `created_at`.
    '''
    if request.method == 'GET':
        list = ListStyle().list(Place.select(), request)
        return jsonify(list), 200

    elif request.method == 'POST':
        params = request.values
        place = Place()

        '''Check that all the required parameters are made in request.'''
        required = set(["owner", "city", "name"]) <= set(request.values.keys())
        if required is False:
            return jsonify(msg="Missing parameter."), 400

        for key in params:
            if key == 'updated_at' or key == 'created_at':
                continue
            setattr(place, key, params.get(key))
        place.save()
        return jsonify(place.to_dict()), 200


@app.route('/places/<int:place_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_place_id(place_id):
    '''Select the place with the id from the database and store as the variable
    `place`. Return that place's hash with a GET request method. Update the
    attributes, excepting  `owner` and `city` of the place with PUT request
    method. Remove the the place with this id from the database with a DELETE
    request method. Will not set attribute passed as `updated_at`,
    `created_at`, `owner`, or `city`.

    Keyword arguments:
    place_id: The id of the place.
    '''
    try:
        place = Place.select().where(Place.id == place_id).get()
    except Place.DoesNotExist:
        raise Exception("There is no place with this id.")

    if request.method == 'GET':
        return jsonify(place.to_dict()), 200

    elif request.method == 'PUT':
        params = request.values
        for key in params:
            if key == 'owner' or key == 'city':
                return jsonify(msg="You may not update the %s." % key), 409
            if key == 'updated_at' or key == 'created_at':
                continue
            else:
                setattr(place, key, params.get(key))
        place.save()
        return jsonify(msg="Place information updated successfully."), 200

    elif request.method == 'DELETE':
        try:
            place = Place.delete().where(Place.id == place_id)
        except Place.DoesNotExist:
            raise Exception("There is no place with this id.")
        place.execute()
        return jsonify(msg="Place deleted successfully."), 200


@app.route('/places/<int:place_id>/available', methods=['POST'])
def handle_place_availibility(place_id):
    '''Checks to see if a place is available on a particular date that is
    passed as parameter with a POST request. Data required is 'year', 'month',
    and 'day'.

    Keyword arguments:
    place_id -- The id of the place to determine if the date is already booked.
    '''
    if request.method == 'POST':
        try:
            Place.select().where(Place.id == place_id).get()
        except Place.DoesNotExist:
            return jsonify("No place exists with this id."), 400

        '''Check that all the required parameters are made in request.'''
        required = set(["year", "month", "day"]) <= set(request.values.keys())
        if required is False:
            return jsonify(msg="Missing parameter."), 400

        date_requested = ''
        for param in ['year', 'month', 'day']:
            date_requested+=request.form[param] + '/'

        book_inquiry = datetime.strptime(date_requested[:-1], "%Y/%m/%d")

        arr = []
        for place_book in (PlaceBook
                           .select()
                           .where(PlaceBook.place == place_id)
                           .iterator()):
            start = place_book.date_start
            end = start + timedelta(days=place_book.number_nights)

            if book_inquiry >= start and book_inquiry < end:
                return jsonify(available=False), 200

        return jsonify(available=True), 200


@app.route('/states/<int:state_id>/places', methods=['GET'])
def handle_place_state_id(state_id):
    '''Retrieve all the places with a state of that passed in the URL.

    Keyword arguments:
    state_id -- The id of the state that this place belongs.
    '''
    if request.method == 'GET':
        try:
            State.select().where(State.id == state_id).get()
        except State.DoesNotExist:
            return jsonify("No state exists with this id."), 400

        list = ListStyle().list((Place
                                .select()
                                .join(City)
                                .join(State)
                                .where(State.id == state_id)), request)

        return jsonify(list), 200


@app.route('/states/<int:state_id>/cities/<int:city_id>/places',
           methods=['GET', 'POST'])
def handle_place_city_id(state_id, city_id):
    '''With a GET request method, select the places belonging to the particular
    city (based on the city id) and store their hashes in an array to be
    returned. Will not set attribute passed as `updated_at` or `created_at`.

    Keyword arguments:
    state_id: The id of the place.
    city_id: The id of the city.
    '''

    if request.method == 'GET':
        try:
            places = Place.select().where(Place.city == city_id).get()
        except Place.DoesNotExist:
            return jsonify("There is no place with this id, in this state."),
            400

        arr = []
        for place in Place.select().where(Place.city == city_id):
            arr.append(place.to_dict())
        return jsonify(arr), 200

    elif request.method == 'POST':
        params = request.values
        place = Place()

        '''Check that all the required parameters are made in request.'''
        required = set(["owner", "name"]) <= set(request.values.keys())
        if required is False:
            return jsonify(msg="Missing parameter."), 400

        for key in params:
            if key == 'updated_at' or key == 'created_at':
                continue
            setattr(place, key, params.get(key))

        place.city = city_id
        place.save()
        return jsonify(place.to_dict()), 200
