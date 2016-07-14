from flask import Flask
from flask import request, make_response, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model
from app.models.city import City
from app import app
from app.models.base import db
import json


@app.route('/states/<int:state_id>/cities', methods=['GET', 'POST'])
def handle_cities(state_id):
    if request.method == 'POST':
        for city in City.select():
            if str(request.form['name']) == city.name:
                return make_response(jsonify(code=10002,
                                             msg="City already exists in this state"), 409)
        city = City.create(city=request.form['city'],
                           state=request.form['state'])
        return city.to_hash()
    else:
        arr = []
        for city in City.select().where(State.id == state_id):
            arr.append(model_to_dict(city, exclude=[City.created_at, City.updated_at]))
        cities = json.dumps(arr)
        return cities


@app.route('/states/<int:state_id>/cities/<int:city_id>', methods=['GET', 'DELETE'])
def handle_city_id(state_id, city_id):
    arr = []
    for city in City.select():
        if str(city_id) == str(city.id):
            this_city = city
    if request.method == 'GET':
        arr.append(model_to_dict(this_city, exclude=[City.created_at, City.updated_at]))
        return json.dumps(arr)

    elif request.method == 'DELETE':
        q = City.delete().where(City.id == city_id)
        q.execute()
        return "deleted"
