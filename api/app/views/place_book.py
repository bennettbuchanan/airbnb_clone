from flask import Flask, request, make_response, jsonify
from app.models.place_book import PlaceBook
from app import app
import time


@app.route('/places/<int:place_id>/books', methods=['GET', 'POST'])
def handle_books(place_id):
    '''Returns all bookings as JSON objects in an array with a GET
    request. Adds a booking to the place_id with a POST request.

    Keyword arguments:
    place_id: The id of the place with the booking.
    '''
    if request.method == 'GET':
        arr = []
        for book in PlaceBook.select().where(PlaceBook.place == place_id).iterator():
            arr.append(book.to_hash())
        return jsonify(arr), 200

    elif request.method == 'POST':
        params = request.values
        book = PlaceBook()
        for key in params:
            if key == 'date_start':
                try:
                    time.strptime(params.get(key), "%Y/%m/%d %H:%M:%S")
                    setattr(book, key, params.get(key))
                except ValueError:
                    raise ValueError("Incorrect time format, should be " +
                                     "yyyy/MM/dd HH:mm:ss")
            else:
                setattr(book, key, params.get(key))
        book.place = place_id
        book.save()
        return jsonify(book.to_hash()), 200


@app.route('/places/<int:place_id>/books/<int:book_id>',
           methods=['GET', 'PUT', 'DELETE'])
def handle_books_id(place_id, book_id):
    '''Returns a JSON object of the book_id with a GET request method. Updates
    a booking's attributes with a POST request method. Removes a booking with a
    DELETE request method.

    Keyword arguments:
    place_id: The id of the place with the booking.
    book_id: The id of the booking.
    '''
    try:
        book = PlaceBook.select().where(PlaceBook.id == book_id).get()
    except PlaceBook.DoesNotExist:
        raise Exception("There is no placebook with this id.")

    if request.method == 'GET':
        return jsonify(book.to_hash()), 200

    elif request.method == 'PUT':
        params = request.values
        for key in params:
            if key == 'user':
                raise Exception("You may not change the user.")
            else:
                setattr(book, key, params.get(key))
        book.save()
        return make_response(jsonify(msg="Place book information updated " +
                                     "successfully."), 200)

    elif request.method == 'DELETE':
        try:
            book = PlaceBook.delete().where(PlaceBook.id == book_id)
        except PlaceBook.DoesNotExist:
            raise Exception("There is no place with this id.")
        book.execute()
        return make_response(jsonify(msg="Place book deleted successfully."),
                             200)
