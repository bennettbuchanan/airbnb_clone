from flask import Flask
from flask import request, make_response, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model
from app.models.state import State
from app import app
from app.models.base import db
import json


@app.route('/states', methods=['GET', 'POST'])
def handle_states():
    if request.method == 'POST':
        for state in State.select():
            if str(request.form['name']) == state.name:
                return make_response(jsonify(code=10001,
                                             msg="State already exists"), 409)
        state = State.create(name=request.form['name'])
        return state.to_hash()
    else:
        arr = []
        for state in State.select():
            arr.append(model_to_dict(state, exclude=[State.created_at, State.updated_at]))
        states = json.dumps(arr)
        return states


@app.route('/states/<int:state_id>', methods=['GET', 'DELETE'])
def handle_state_id(state_id):
    arr = []
    for state in State.select():
        if str(state_id) == str(state.id):
            this_state = state
    if request.method == 'GET':
        arr.append(model_to_dict(this_state, exclude=[State.created_at, State.updated_at]))
        return json.dumps(arr)

    elif request.method == 'DELETE':
        q = State.delete().where(State.id == state_id)
        q.execute()
        return "deleted"
