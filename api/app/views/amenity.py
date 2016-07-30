from flask import request, jsonify
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.place_amenity import PlaceAmenities
from return_styles import ListStyle
from app import app


@app.route('/amenities', methods=['GET', 'POST'])
def handle_amenity():
    '''Returns all amenities as JSON objects in an array with a GET request.
    Adds an amenity with a POST request.
    '''
    if request.method == 'GET':
        list = ListStyle().list(Amenity.select(), request)
        return jsonify(list), 200

    elif request.method == 'POST':
        try:
            Amenity.select().where(Amenity.name == request.form['name']).get()
            return jsonify(code=10003, msg="Name already exists"), 409
        except Amenity.DoesNotExist:
            '''Check that all the required parameters are made in request.'''
            required = set(["name"]) <= set(request.values.keys())
            if required is False:
                return jsonify(msg="Missing parameter."), 400

            amenity = Amenity.create(name=request.form['name'])
            return jsonify(amenity.to_dict()), 200


@app.route('/amenities/<int:amenity_id>', methods=['GET', 'DELETE'])
def handle_amenity_id(amenity_id):
    '''Returns a JSON object of the amenity with the id passed as parameter
    with a GET request method. Removes an amenity with DELETE request method.

    Keyword arguments:
    amenity_id: The id of the amenity.
    '''
    try:
        amenity = Amenity.select().where(Amenity.id == amenity_id).get()
    except Amenity.DoesNotExist:
        raise Exception("There is no amenity with this id.")

    if request.method == 'GET':
        return jsonify(amenity.to_dict()), 200

    elif request.method == 'DELETE':
        amenity = Amenity.delete().where(Amenity.id == amenity_id)
        amenity.execute()
        return jsonify(msg="Amenity deleted successfully."), 200


@app.route('/places/<int:place_id>/amenities', methods=['GET'])
def handle_place_id_amenity(place_id):
    '''Returns all amenities of the place_id as JSON objects in an array with a
    GET request.

    Keyword arguments:
    place_id: The id of the amenity.
    '''
    try:
        PlaceAmenities.select().where(PlaceAmenities.place == place_id).get()
    except PlaceAmenities.DoesNotExist:
        return jsonify(msg="Amenity does not exist."), 404

    if request.method == 'GET':
        '''Use a join statement to get the instances in the amenity table.'''
        list = ListStyle().list((Amenity
                                 .select()
                                 .join(PlaceAmenities,
                                       on=PlaceAmenities.amenity)
                                 .where(PlaceAmenities.place == place_id)),
                                request)

        return jsonify(list), 200


@app.route('/places/<int:place_id>/amenities/<int:amenity_id>',
           methods=['POST', 'DELETE'])
def handle_amenity_for_place(place_id, amenity_id):
    '''Add the amenity with `amenity_id` to the place with `place_id` with a
    POST request. Delete the amenity with the id of `amenity_id` with a DELETE
    request.

    Keyword arguments:
    place_id -- The id of the place.
    amenity_id -- The id of the amenity.
    '''
    try:
        Amenity.select().where(Amenity.id == amenity_id).get()
    except Amenity.DoesNotExist:
        return jsonify(msg="Amenity does not exist."), 404
    try:
        Place.select().where(Place.id == place_id).get()
    except Place.DoesNotExist:
        return jsonify(msg="Place does not exist."), 404

    if request.method == 'POST':
        '''Save the connection in the ReviewPlace table.'''
        PlaceAmenities().create(place=place_id, amenity=amenity_id)

        return jsonify(msg="Amenity added to place successfully."), 201

    elif request.method == 'DELETE':
        (PlaceAmenities
         .delete()
         .where((PlaceAmenities.place == place_id) &
                (PlaceAmenities.amenity == amenity_id))
         .execute())

        Amenity.delete().where(Amenity.id == amenity_id).execute()

        return jsonify(msg="Amenity deleted successfully."), 200
