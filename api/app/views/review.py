from flask import Flask, request, make_response, jsonify
from app.models.user import User
from app.models.review import Review
from app.models.place import Place
from app.models.review_user import ReviewUser
from app.models.review_place import ReviewPlace
from app import app


@app.route('/users/<int:user_id>/reviews', methods=['GET', 'POST'])
def handle_reviews(user_id):
    '''Returns the reviews of the user passed the argument `user_id`. This is
    accomplished through querying the ReviewUser table, and returning rows in
    which `user_id` is equal to the id of a user. Then, using the
    ForeignKeyField, retrieve those particular reviews with the to_hash()
    method.

    Keyword arguments:
    user_id = The id of the user that is being reviewed.
    '''
    try:
        User.select().where(User.id == user_id).get()
    except User.DoesNotExist:
        return make_response(jsonify(msg="There is no user with this id."),
                             404)

    if request.method == 'GET':
        arr = []
        for review_user in ReviewUser.select().where(ReviewUser.user == user_id):
            arr.append(review_user.review.to_hash())
        return jsonify(arr), 200

    elif request.method == 'POST':
        params = request.values
        review = Review()

        for key in params:
            setattr(review, key, params.get(key))

        if review.message is None or review.user_id is None:
            return make_response(jsonify(msg="Missing required data."), 404)

        review.save()

        '''Save the connection in the ReviewUser table.'''
        ReviewUser().create(user=user_id, review=review.id)

        return jsonify(review.to_hash()), 201


@app.route('/users/<int:user_id>/my_reviews', methods=['GET'])
def handle_my_reviews(user_id):
    '''Returns all the reviews from the database of the user as JSON objects
    with a GET request.

    Keyword Arguments:
    user_id = The id of the user that wrote the review.
    '''
    if request.method == 'GET':
        arr = []
        for review in Review.select().where(Review.user == user_id):
            arr.append(review.to_hash())
        return jsonify(arr), 200


@app.route('/users/<int:user_id>/reviews/<int:review_id>',
           methods=['GET', 'DELETE'])
def handle_review_id(user_id, review_id):
    '''Gets the review with the id of the parameter `review_id`.

    Keyword arguments:
    user_id -- The id of the user with the review.
    review_id -- The id of the the review.
    '''
    try:
        this_review = ReviewUser.select().where(
                        (ReviewUser.user == user_id) &
                        (ReviewUser.review == review_id)).get()
    except ReviewUser.DoesNotExist:
        return make_response(jsonify(msg="Review does not exist."), 404)

    if request.method == 'GET':
        return jsonify([this_review.review.to_hash()]), 200

    elif request.method == 'DELETE':
        ReviewUser.delete().where((ReviewUser.user == user_id) &
                                  (ReviewUser.review == review_id)).execute()

        Review.delete().where(Review.id == review_id).execute()
        return make_response(jsonify(msg="Review deleted successfully."), 200)


@app.route('/places/<int:place_id>/reviews', methods=['GET', 'POST'])
def handle_place_reviews(place_id):
    '''Returns an array of reviews of the place with the same id as that of
    the parameter `place_id` with a GET request. Creates a new review with
    the place_id.

    Keyword arguments:
    place_id -- The id of the place to be reviewed.
    '''
    try:
        Place.select().where(Place.id == place_id).get()
    except Place.DoesNotExist:
        return make_response(jsonify(msg="Place does not exist."), 404)

    if request.method == 'GET':
        arr = []
        for review_place in ReviewPlace.select().where(ReviewPlace.place == place_id):
            arr.append(review_place.review.to_hash())
        return jsonify(arr), 200

    elif request.method == 'POST':
        params = request.values
        review = Review()

        for key in params:
            setattr(review, key, params.get(key))

        review.save()

        '''Save the connection in the ReviewPlace table.'''
        ReviewPlace().create(place=place_id, review=review.id)

        return jsonify(review.to_hash()), 201


@app.route('/places/<int:place_id>/reviews/<int:review_id>',
           methods=['GET', 'DELETE'])
def handle_place_review(place_id, review_id):
    '''Gets the review with the id of the parameter `review_id`.

    Keyword arguments:
    place_id -- The id of the place with the review.
    review_id -- The id of the the review.
    '''
    try:
        this_review = ReviewPlace.select().where(
                        (ReviewPlace.place == place_id) &
                        (ReviewPlace.review == review_id)).get()
    except ReviewPlace.DoesNotExist:
        return make_response(jsonify(msg="Review does not exist."), 404)

    if request.method == 'GET':
        return jsonify([this_review.review.to_hash()]), 200

    elif request.method == 'DELETE':
        ReviewPlace.delete().where((ReviewPlace.place == place_id) &
                                   (ReviewPlace.review == review_id)).execute()

        Review.delete().where(Review.id == review_id).execute()
        return make_response(jsonify(msg="Review deleted successfully."),
                             200)
