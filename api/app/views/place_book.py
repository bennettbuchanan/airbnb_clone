from flask import request, jsonify
from datetime import datetime, timedelta
from app.models.place_book import PlaceBook
from return_styles import ListStyle
from app import app


@app.route('/places/<int:place_id>/books', methods=['GET', 'POST'])
def handle_books(place_id):
    '''Returns all bookings as JSON objects in an array with a GET
    request. Adds a booking to the place_id with a POST request.

    Keyword arguments:
    place_id: The id of the place with the booking.
    '''
    if request.method == 'GET':
        list = ListStyle().list((PlaceBook
                                 .select()
                                 .where(PlaceBook.place == place_id)),
                                request)
        return jsonify(list), 200

    elif request.method == 'POST':
        try:
            datetime.strptime(request.form['date_start'], "%Y/%m/%d %H:%M:%S")
        except ValueError:
            return jsonify(msg="Incorrect time format: should be " +
                           "yyyy/MM/dd HH:mm:ss"), 409

        '''Convert the date_start into a date without time.'''
        book_inquiry = datetime.strptime(request.form['date_start'],
                                         "%Y/%m/%d %H:%M:%S").date()

        arr = []
        for place_book in (PlaceBook
                           .select()
                           .where(PlaceBook.place == place_id)
                           .iterator()):
            start = place_book.date_start.date()
            end = start + timedelta(days=place_book.number_nights)

            '''Check to see if book_inquiry date is not taken.'''
            if book_inquiry >= start and book_inquiry < end:
                return jsonify(available=False), 200

        params = request.values
        book = PlaceBook()

        '''Check that all the required parameters are made in request.'''
        required = set(["date_start", "user"]) <= set(request.values.keys())
        if required is False:
            return jsonify(msg="Missing parameter."), 400

        for key in params:
            if key == 'updated_at' or key == 'created_at':
                continue
            setattr(book, key, params.get(key))
        book.place = place_id
        book.save()
        return jsonify(book.to_dict()), 200


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
        return jsonify(book.to_dict()), 200

    elif request.method == 'PUT':
        params = request.values
        for key in params:
            if key == 'user':
                return jsonify(msg="You may not change the user."), 409
            if key == 'updated_at' or key == 'created_at':
                continue
            setattr(book, key, params.get(key))
        book.save()
        return jsonify(msg="Place book information updated successfully."), 200

    elif request.method == 'DELETE':
        try:
            book = PlaceBook.delete().where(PlaceBook.id == book_id)
        except PlaceBook.DoesNotExist:
            raise Exception("There is no place with this id.")
        book.execute()
        return jsonify(msg="Place book deleted successfully."), 200
