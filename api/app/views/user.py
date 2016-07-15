from flask import Flask, request, make_response, jsonify
from app.models.user import User
from app import app


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    '''Returns all the users from the database as JSON objects with a GET
    request, or adds a new user to the database with a POST request. Refer to
    exception rules of peewee `get()` method for additional explanation of
    how the POST request is handled:
    http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery.get
    '''
    if request.method == 'GET':
        arr = []
        for user in User.select():
            arr.append(user.to_hash())
        return jsonify(arr), 200

    elif request.method == 'POST':
        try:
            User.select().where(User.email == request.form['email']).get()
            return make_response(jsonify(code=10000,
                                         msg="Email already exists"), 409)
        except User.DoesNotExist:
            params = request.values
            user = User()
            for key in params:
                setattr(user, key, params.get(key))
            user.save()
            return jsonify(user.to_hash()), 200


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user_id(user_id):
    '''Select the user with the id from the database and store as the variable
    `user` with a GET request method. Update the data of the particular user
    with a PUT request method. This will take the parameters passed and update
    only those values. Note that attempting to update the email of the user,
    or values that the user does not have as attributes will result in their
    respect exceptions. Remove the user with this id from the database with
    a DELETE request method.

    Keyword arguments:
    user_id: The id of the user from the database.
    '''
    try:
        user = User.select().where(User.id == user_id).get()
    except User.DoesNotExist:
        raise Exception("There is no user with this id.")

    if request.method == 'GET':
        return jsonify(user.to_hash()), 200

    elif request.method == 'PUT':
        params = request.values
        for key in params:
            if key == 'email':
                raise Exception("You may not change the user's email.")
            else:
                setattr(user, key, params.get(key))
        user.save()
        return make_response(jsonify(msg="User information updated " +
                                     "successfully."), 200)

    elif request.method == 'DELETE':
        try:
            user = User.delete().where(User.id == user_id)
        except User.DoesNotExist:
            raise Exception("There is no user with this id.")
        user.execute()
        return make_response(jsonify(msg="User deleted successfully."), 200)