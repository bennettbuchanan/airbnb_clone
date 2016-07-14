from flask import Flask
from flask import request, make_response, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from app import app
from app.models.base import db
import json


@app.route('/amenities', methods=['GET', 'POST'])
def handle_amenity():
    if request.method == 'POST':
        for place_book in Amenity.select():
            if str(request.form['name']) == place_book.name:
                return make_response(jsonify(code=10003,
                                             msg="Name already exists"), 409)
        place_book = Amenity.create(name=request.form['name'])
        return place_book.to_hash()
    else:
        arr = []
        for place_book in Amenity.select():
            arr.append(model_to_dict(place_book, exclude=[Amenity.created_at, Amenity.updated_at]))
        books = json.dumps(arr)
        return books

@app.route('/amenities/<int:amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_amenity_id(amenity_id):
    arr = []
    for amenity in Amenity.select().where(Amenity.id == amenity_id):
        if str(amenity_id) == str(amenity.id):
            this_amenity = amenity
    if request.method == 'GET':
        arr.append(model_to_dict(this_amenity, exclude=[Amenity.created_at, Amenity.updated_at]))
        return json.dumps(arr)

    elif request.method == 'DELETE':
        q = Amenity.delete().where(Amenity.id == amenity_id)
        q.execute()
        return "deleted"


@app.route('/places/<int:place_id>/amenities', methods=['GET'])
def handle_place_id_amenity(place_id):
    arr = []
    for placeamenity in PlaceAmenities.select().where(PlaceAmenities.id == place_id):
        if str(placeamenity_id) == str(placeamenity.id):
            this_placeamenity = placeamenity
    if request.method == 'GET':
        arr.append(model_to_dict(this_placeamenity, exclude=[PlaceAmenities.created_at, PlaceAmenities.updated_at]))
        return json.dumps(arr)
