from flask import request, jsonify
from app.models.user import User
from return_styles import ListStyle
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
        list = ListStyle().list(User.select(), request)
        return jsonify(list), 200

    elif request.method == 'POST':
        try:
            User.select().where(User.email == request.form['email']).get()
            return jsonify(code=10000, msg="Email already exists"), 409
        except User.DoesNotExist:
            params = request.values
            user = User()

            '''Check that all the required parameters are made in request.'''
            required = set(["first_name", "last_name", "email",
                            "password"]) <= set(params.keys())
            if required is False:
                return jsonify(msg="Missing parameter."), 400

            for key in params:
                if key == 'updated_at' or key == 'created_at':
                    continue
                setattr(user, key, params.get(key))
            user.save()
            return jsonify(user.to_dict()), 201


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
        return jsonify(msg="User does not exist."), 404

    if request.method == 'GET':
        return jsonify(user.to_dict()), 200

    elif request.method == 'PUT':
        params = request.values
        for key in params:
            if key == 'email':
                return jsonify(msg="You may not change the user's email."), 409
            if key == 'updated_at' or key == 'created_at':
                continue
            else:
                setattr(user, key, params.get(key))
        user.save()
        return jsonify(msg="User information updated successfully."), 201

    elif request.method == 'DELETE':
        try:
            user = User.delete().where(User.id == user_id)
        except User.DoesNotExist:
            return jsonify(msg="User does not exist."), 200
        user.execute()
        return jsonify(msg="User deleted successfully."), 200
