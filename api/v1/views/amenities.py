#!/usr/bin/python3
"""Handles REST operations for amentites object"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from flask import make_response
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=["GET", "POST"])
def get_amenity():
    if request.method == "GET":
        return jsonify([amenity.to_dict()
                       for amenity in storage.all(Amenity).values()])
    else:
        new_dict = request.get_json()
        if new_dict:
            if new_dict.get("name"):
                amenity = Amenity(**new_dict)
                amenity.save()
                return make_response(jsonify(amenity.to_dict()), 201)
            else:
                return make_response({"error": "Missing name"}, 400)
        else:
            return make_response({"error": "Not a JSON"}, 400)


@app_views.route("/amenities/<amentiy_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def handel_amentiy(amentiy_id):
    amentiy = storage.get(Amenity, amentiy_id)
    if amentiy:
        if request.method == "GET":
            return jsonify(amentiy.to_dict())
        elif request.method == "DELETE":
            amentiy.delete()
            storage.save()
            return jsonify({})
        else:
            new_dict = request.get_json()
            if new_dict:
                for k, v in new_dict.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(amentiy, k, v)  # risk
                amentiy.save()
                return jsonify(amentiy.to_dict())
            else:
                return make_response({"error": "Not a JSON"}, 400)
    abort(404)
