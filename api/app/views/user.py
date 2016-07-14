from flask import Flask
from flask import request
from app.models.user import User
from app import app
from app.models.base import db


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        user = User.create(first_name=request.form['first_name'],
                           last_name=request.form['last_name'],
                           email=request.form['email'],
                           password=request.form['password'])
        return user.to_hash()
    else:
        arr = []
        for user in User.select():
            arr.append(user.first_name)

        return str(arr)
