from flask import Flask
from flask import request, make_response, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model
from app.models.user import User
from app import app
from app.models.base import db
import json


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        for user in User.select():
            if str(request.form['email']) == user.email:
                return make_response(jsonify(code=10000,
                                             msg="Email already exists"), 409)
        user = User.create(first_name=request.form['first_name'],
                           last_name=request.form['last_name'],
                           email=request.form['email'],
                           password=request.form['password'])
        return user.to_hash()
    else:
        arr = []
        for user in User.select():
            arr.append(model_to_dict(user, exclude=[User.created_at, User.updated_at]))
        test = json.dumps(arr)
        return test


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user_id(user_id):
    arr = []
    for user in User.select():
        if str(user_id) == str(user.id):
            this_user = user
    if request.method == 'GET':
        arr.append(model_to_dict(this_user, exclude=[User.created_at, User.updated_at]))
        return json.dumps(arr)

    elif request.method == 'PUT':
        params = dict([p.split('=') for p in request.get_data().split('&')])
        for key in params:
            if str(key) == 'id':
                this_user.id = params.get(key)
            if str(key) == 'created_at':
                this_user.created_at = params.get(key)
            if str(key) == 'updated_at':
                this_user.updated_at = params.get(key)
            if str(key) == 'first_name':
                this_user.first_name = params.get(key)
            if str(key) == 'last_name':
                this_user.last_name = params.get(key)
            if str(key) == 'is_admin':
                this_user.is_admin = params.get(key)
            this_user.save()
        return "user changed"

    elif request.method == 'DELETE':
        q = User.delete().where(User.id == user_id)
        q.execute()
        return "deleted"
