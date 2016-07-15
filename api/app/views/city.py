from flask import Flask, request, make_response, jsonify
from app.models.state import State
from app.models.city import City
from app import app


@app.route('/states/<int:state_id>/cities', methods=['GET', 'POST'])
def handle_city(state_id):
    '''Returns all the cities in the state with the id passed as `state_id`
    from the database as JSON objects with a GET request, or adds a new state
    to the database with a POST request. Refer to exception rules of peewee
    `get()` method for additional explanation of how the POST request is
    handled:
    http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery.get
    '''
    if request.method == 'GET':
        arr = []
        for city in City.select().where(City.state == state_id):
            arr.append(city.to_hash())
        return jsonify(arr), 200

    elif request.method == 'POST':
        params = request.values
        try:
            City.select().where((City.city == request.form['city']) &
                                (City.state == state_id)
                                ).get()
            return make_response(jsonify(code=10002,
                                         msg="City already exists in this " +
                                         "state"), 409)
        except City.DoesNotExist:
            city = City.create(city=request.form['city'], state=state_id)
            return jsonify(city.to_hash()), 200


@app.route('/states/<int:state_id>/cities/<int:city_id>',
           methods=['GET', 'DELETE'])
def handle_city_id(state_id, city_id):
    '''Select the city with the id from the database and store as the variable
    `city` with a GET request method. Remove the city with this id from the
    database with a DELETE request method.

    Keyword arguments:
    state_id: The state of the city from the database.
    city_id: The id of the city from the database.
    '''
    try:
        city = City.select().where((City.id == city_id) &
                                   (City.state == state_id)
                                   ).get()
    except City.DoesNotExist:
        raise Exception("There is no city with this id, in this state.")

    if request.method == 'GET':
        return jsonify(city.to_hash())

    elif request.method == 'DELETE':
        try:
            city = City.delete().where((City.id == city_id) &
                                       (City.state == state_id))
        except City.DoesNotExist:
            raise Exception("There is no city with this id, in this state.")
        city.execute()
        return make_response(jsonify(msg="City deleted successfully."), 200)