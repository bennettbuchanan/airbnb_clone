from flask import Flask, request, make_response, jsonify
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.place_amenity import PlaceAmenities
from app import app


@app.route('/amenities', methods=['GET', 'POST'])
def handle_amenity():
    '''Returns all amenities as JSON objects in an array with a GET request.
    Adds an amenity with a POST request.
    '''
    if request.method == 'GET':
        arr = []
        for amenity in Amenity.select():
            arr.append(amenity.to_hash())
        return jsonify(arr), 200

    elif request.method == 'POST':
        try:
            Amenity.select().where(Amenity.name == request.form['name']).get()
            return make_response(jsonify(code=10003, msg="Name already " +
                                         "exists"), 409)
        except Amenity.DoesNotExist:
            params = request.values
            amenity = Amenity()
            for key in params:
                setattr(amenity, key, params.get(key))
            amenity.save()
            return jsonify(amenity.to_hash()), 200


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
        return jsonify(amenity.to_hash()), 200

    elif request.method == 'DELETE':
        amenity = Amenity.delete().where(Amenity.id == amenity_id)
        amenity.execute()
        return make_response(jsonify(msg="Amenity deleted successfully."), 200)


@app.route('/places/<int:place_id>/amenities', methods=['GET'])
def handle_place_id_amenity(place_id):
    '''Returns all amenities of the place_id as JSON objects in an array with a GET
    request.

    Keyword arguments:
    place_id: The id of the amenity.
    '''
    if request.method == 'GET':
        arr = []
        query = (Amenity
                 .select()
                 .join(PlaceAmenities)
                 .join(Place)
                 .where(Place.id == place_id))
        for amenity in query:
            arr.append(amenity.to_hash())
        return jsonify(arr), 200
