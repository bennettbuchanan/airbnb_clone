from flask import request, jsonify
from app.models.state import State
from app.models.city import City
from return_styles import ListStyle
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
        list = ListStyle().list((City
                                 .select()
                                 .where(City.state == state_id)),
                                request)
        return jsonify(list), 200

    elif request.method == 'POST':
        try:
            City.select().where((City.name == request.form['name']) &
                                (City.state == state_id)
                                ).get()
            return jsonify(code=10002, msg="City already exists in this " +
                           "state"), 409
        except City.DoesNotExist:
            '''Check that all the required parameters are made in request.'''
            required = set(["name"]) <= set(request.values.keys())
            if required is False:
                return jsonify(msg="Missing parameter."), 400
            city = City.create(name=request.form['name'], state=state_id)
            return jsonify(city.to_dict()), 200


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
        raise jsonify(msg="There is no city with this id in this state."), 400

    if request.method == 'GET':
        return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        try:
            city = City.delete().where((City.id == city_id) &
                                       (City.state == state_id))
        except City.DoesNotExist:
            raise Exception("There is no city with this id, in this state.")
        city.execute()
        return jsonify(msg="City deleted successfully."), 200
