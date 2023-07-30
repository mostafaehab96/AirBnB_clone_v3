#!/usr/bin/python3
"""Handles REST operations for City object"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from flask import make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<string:state_id>/cities", strict_slashes=False, methods=["GET", "POST"])
def cities_by_state(state_id):
    state = storage.get(State, state_id)
    if state:
        if request.method == "GET":
            return jsonify([city.to_dict() for city in state.cities])
        else:
            new_dict = request.get_json()
            if new_dict:
                if new_dict.get("name"):
                    city = City(**new_dict)
                    state.cities.append(city)
                    city.save()
                    city_dict = city.to_dict()
                    del city_dict['state']
                    return make_response(jsonify(city_dict), 201)
                else:
                    return make_response({"error": "Missing name"}, 400)
            else:
                return make_response({"error": "Not a JSON"}, 400)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def city_byid(city_id):
    city = storage.get(City, city_id)
    if city:
        if request.method == "GET":
            return jsonify(city.to_dict())
        elif request.method == "DELETE":
            city.delete()
            storage.save()
            return jsonify({})
        else:
            new_dict = request.get_json()
            if new_dict:
                for k, v in new_dict.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(city, k, v)  # risk
                city.save()
                return jsonify(city.to_dict())
            else:
                return make_response({"error": "Not a JSON"}, 400)
    abort(404)
