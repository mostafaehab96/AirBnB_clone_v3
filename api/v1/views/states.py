#!/usr/bin/python3
"""Handles REST operations for State object"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from flask import make_response
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET", "POST"])
def states():
    if request.method == "GET":
        return jsonify([state.to_dict()
                       for state in storage.all(State).values()])
    else:
        new_dict = request.get_json()
        if new_dict:
            if new_dict.get("name"):
                state = State(**new_dict)
                state.save()
                return make_response(jsonify(state.to_dict()), 201)
            else:
                return make_response({"error": "Missing name"}, 400)
        else:
            return make_response({"error": "Not a JSON"}, 400)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def state(state_id):
    state = storage.get(State, state_id)
    if state:
        if request.method == "GET":
            return jsonify(state.to_dict())
        elif request.method == "DELETE":
            state.delete()
            storage.save()
            return jsonify({})
        else:
            new_dict = request.get_json()
            if new_dict:
                for k, v in new_dict.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(state, k, v)
                state.save()
                return jsonify(state.to_dict())
            else:
                return make_response({"error": "Not a JSON"}, 400)
    abort(404)
