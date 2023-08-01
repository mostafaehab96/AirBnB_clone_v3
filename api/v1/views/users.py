#!/usr/bin/python3
"""Handles REST operations for User object"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from flask import make_response
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET", "POST"])
def get_users():
    if request.method == "GET":
        return jsonify([user.to_dict()
                       for user in storage.all(User).values()])
    else:
        new_dict = request.get_json()
        if new_dict:
            if not new_dict.get("email"):
                return make_response({"error": "Missing email"}, 400)
            elif not new_dict.get("password"):
                return make_response({"error": "Missing password"}, 400)
            else:
                user = User(**new_dict)
                user.save()
                return make_response(jsonify(user.to_dict()), 201)
        else:
            return make_response({"error": "Not a JSON"}, 400)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def handel_user(user_id):
    user = storage.get(User, user_id)
    if user:
        if request.method == "GET":
            return jsonify(user.to_dict())
        elif request.method == "DELETE":
            user.delete()
            storage.save()
            return jsonify({})
        else:
            new_dict = request.get_json()
            if new_dict:
                for k, v in new_dict.items():
                    if k not in ['id', 'created_at', 'updated_at', 'email']:
                        setattr(user, k, v)  # risk
                user.save()
                return jsonify(user.to_dict())
            else:
                return make_response({"error": "Not a JSON"}, 400)
    abort(404)
