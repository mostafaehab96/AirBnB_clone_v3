#!/usr/bin/python3
"""Handles REST operations for Review object"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from flask import make_response
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET", "POST"])
def reviews_by_place(place_id):
    place = storage.get(Place, place_id)
    if place:
        if request.method == "GET":
            return jsonify([review.to_dict() for review in place.reviews])
        else:
            new_dict = request.get_json()
            if new_dict:
                if not new_dict.get("user_id"):
                    return make_response({"error": "Missing user_id"}, 400)
                if not storage.get(User, new_dict['user_id']):
                    abort(404)
                if not new_dict.get("text"):
                    return make_response({"error": "Missing text"}, 400)
                else:
                    review = Review(**new_dict)
                    place.reviews.append(review)
                    review.save()
                    review_dict = review.to_dict()
                    print(review_dict)
                    del review_dict['place']
                    return make_response(jsonify(review_dict), 201)
            else:
                return make_response({"error": "Not a JSON"}, 400)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def review_byid(review_id):
    review = storage.get(Review, review_id)
    if review:
        if request.method == "GET":
            return jsonify(review.to_dict())
        elif request.method == "DELETE":
            review.delete()
            storage.save()
            return jsonify({})
        else:
            new_dict = request.get_json()
            if new_dict:
                for k, v in new_dict.items():
                    if k not in ['id', 'user_id', 'place_id',
                                 'created_at', 'updated_at']:
                        setattr(review, k, v)
                review.save()
                return jsonify(review.to_dict())
            else:
                return make_response({"error": "Not a JSON"}, 400)
    abort(404)
