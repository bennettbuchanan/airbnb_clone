from flask import Flask
from flask import request, make_response, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model
from app.models.place_book import PlaceBook
from app import app
from app.models.base import db
import json


@app.route('/places/<int:place_id>/books', methods=['GET', 'POST'])
def handle_books(place_id):
    if request.method == 'POST':
        for place_book in PlaceBook.select():
            if str(request.form['name']) == place_book.name:
                return make_response(jsonify(code=10002,
                                             msg="PlaceBook already exists in this state"), 409)
        place_book = PlaceBook.create(place=request.form['place'],
                                      is_validated=request.form['is_validated'],
                                      date_start=request.form['date_start'],
                                      number_nights=request.form['number_nights'])
        return place_book.to_hash()
    else:
        arr = []
        for place_book in PlaceBook.select().where(PlaceBook.id == place_id):
            arr.append(model_to_dict(place_book, exclude=[PlaceBook.created_at, PlaceBook.updated_at]))
        books = json.dumps(arr)
        return books


@app.route('/places/<int:place_id>/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_books_id(place_id, book_id):
    arr = []
    for book in PlaceBook.select():
        if str(book_id) == str(book.id):
            this_book = book
    if request.method == 'GET':
        arr.append(model_to_dict(this_book, exclude=[PlaceBook.created_at, PlaceBook.updated_at]))
        return json.dumps(arr)

    elif request.method == 'PUT':
        params = dict([p.split('=') for p in request.get_data().split('&')])
        for key in params:
            if str(key) == 'place':
                this_user.place = params.get(key)
            if str(key) == 'user':
                this_user.user = params.get(key)
            if str(key) == 'is_validated':
                this_user.is_validated = params.get(key)
            if str(key) == 'date_start':
                this_user.date_start = params.get(key)
            if str(key) == 'number_nights':
                this_user.number_nights = params.get(key)
            this_user.save()
        return "user changed"

    elif request.method == 'DELETE':
        q = PlaceBook.delete().where(PlaceBook.id == book_id)
        q.execute()
        return "deleted"
