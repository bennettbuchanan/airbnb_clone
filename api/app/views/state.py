from flask import Flask, request, make_response, jsonify
from app.models.state import State
from app import app


@app.route('/states', methods=['GET', 'POST'])
def handle_states():
    '''Returns all the states from the database as JSON objects with a GET
    request, or adds a new state to the database with a POST request. Refer to
    exception rules of peewee `get()` method for additional explanation of
    how the POST request is handled:
    http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery.get
    '''
    if request.method == 'GET':
        arr = []
        for state in State.select():
            arr.append(state.to_hash())
        return jsonify(arr), 200

    elif request.method == 'POST':
        params = request.values
        try:
            State.select().where(State.name == request.form['name']).get()
            return make_response(jsonify(code=10001,
                                         msg="State already exists"), 409)
        except State.DoesNotExist:
            state = State.create(name=request.form['name'])
            return jsonify(state.to_hash()), 201


@app.route('/states/<int:state_id>', methods=['GET', 'DELETE'])
def handle_state_id(state_id):
    '''Select the state with the id from the database and store as the variable
    `state` with a GET request method. Update the data of the particular state
    with a PUT request method. This will take the parameters passed and update
    only those values. Remove the state with this id from the database with
    a DELETE request method.

    Keyword arguments:
    state_id: The id of the state from the database.
    '''
    try:
        state = State.select().where(State.id == state_id).get()
    except State.DoesNotExist:
        return make_response(jsonify(msg="There is no state with this id."),
                             404)

    if request.method == 'GET':
        return jsonify(state.to_hash()), 200

    elif request.method == 'DELETE':
        try:
            state = State.delete().where(State.id == state_id)
        except State.DoesNotExist:
            raise Exception("There is no state with this id.")
        state.execute()
        return make_response(jsonify(msg="State deleted successfully."), 200)
