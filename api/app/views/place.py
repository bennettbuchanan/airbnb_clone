from flask import Flask
from flask import request, make_response, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model
from app.models.place import Place
from app import app
from app.models.base import db
import json

@app.route('/places', methods=['GET', 'POST'])
def handle_places(state_id):
    if request.method == 'POST':
        for place in Place.select():
            if str(request.form['name']) == place.name:
                return make_response(jsonify(code=10002,
                                             msg="Place already exists in this state"), 409)
        place = Place.create(name=request.form['name'],
                             description=request.form['description'],
                             number_rooms=request.form['number_rooms'],
                             number_bathrooms=request.form['number_bathrooms'],
                             max_guest=request.form['max_guest'],
                             price_by_night=request.form['price_by_night'],
                             latitude=request.form['latitude'],
                             longitude=request.form['longitude'])
        return place.to_hash()
    else:
        arr = []
        for place in Place.select():
            arr.append(model_to_dict(place, exclude=[Place.created_at, Place.updated_at]))
        places = json.dumps(arr)
        return places


@app.route('/places/<int:place_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_place_id(place_id):
    arr = []
    for place in Place.select():
        if str(place_id) == str(place.id):
            this_place = place
    if request.method == 'GET':
        arr.append(model_to_dict(this_place, exclude=[Place.created_at, Place.updated_at]))
        return json.dumps(arr)

    elif request.method == 'PUT':
        params = dict([p.split('=') for p in request.get_data().split('&')])
        for key in params:
            if str(key) == 'name':
                this_place.name = params.get(key)
            if str(key) == 'description':
                this_place.description = params.get(key)
            if str(key) == 'number_rooms':
                this_place.number_rooms = params.get(key)
            if str(key) == 'number_bathrooms':
                this_place.number_bathrooms = params.get(key)
            if str(key) == 'max_guest':
                this_place.max_guest = params.get(key)
            if str(key) == 'price_by_night':
                this_place.price_by_night = params.get(key)
            if str(key) == 'latitude':
                this_place.latitude = params.get(key)
            if str(key) == 'longitude':
                this_place.longitude = params.get(key)
            this_place.save()
        return "place changed"

    elif request.method == 'DELETE':
        q = Place.delete().where(Place.id == place_id)
        q.execute()
        return "deleted"


@app.route('/states/<int:state_id>/cities/<int:city_id>/places', methods=['GET', 'POST'])
def handle_place_city_id(state_id, place_id):
    if request.method == 'GET':
        arr = []
        for place in Place.select().where(Place.id == place_id):
            arr.append(model_to_dict(place, exclude=[Place.created_at, Place.updated_at]))
        places = json.dumps(arr)
        return places
    if request.method == 'POST':
        for place in Place.select():
            if str(request.form['name']) == place.name:
                return make_response(jsonify(code=10002,
                                             msg="Place already exists in this state"), 409)
        place = Place.create(city=request.form['city'],
                             description=request.form['description'],
                             number_rooms=request.form['number_rooms'],
                             number_bathrooms=request.form['number_bathrooms'],
                             max_guest=request.form['max_guest'],
                             price_by_night=request.form['price_by_night'],
                             latitude=request.form['latitude'],
                             longitude=request.form['longitude'])
        return place.to_hash()


# def handle_place_id(state_id, place_id):
#     arr = []
#     for place in Place.select():
#         if str(place_id) == str(place.id):
#             this_place = place
#     if request.method == 'GET':
#         arr.append(model_to_dict(this_place, exclude=[Place.created_at, Place.updated_at]))
#         return json.dumps(arr)
#
#     elif request.method == 'DELETE':
#         q = Place.delete().where(Place.id == place_id)
#         q.execute()
#         return "deleted"
