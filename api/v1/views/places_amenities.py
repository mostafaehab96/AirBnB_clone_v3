#!/usr/bin/python3
"""Handles REST operations for Review object"""

from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from flask import make_response
from models import storage
from models import storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def amenities_by_place(place_id):
    place = storage.get(Place, place_id)
    if place:
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["POST", "DELETE"])
def amenity_byid(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity:
        if request.method == "DELETE":
            if amenity in place.amenities:
                if storage_t == 'db':
                    place.amenities.remove(amenity)
                else:
                    place.amenity_ids.remove(amenity.id)
                place.save()
                return jsonify({})
            else:
                abort(404)
        else:
            if amenity in place.amenities:
                return jsonify(amenity.to_dict())
            else:
                place.amenities.append(amenity)
                place.save()
                return make_response(jsonify(amenity.to_dict()), 201)
    abort(404)
