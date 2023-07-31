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
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET", "POST"])
def places_by_city(city_id):
    city = storage.get(City, city_id)
    if city:
        if request.method == "GET":
            return jsonify([place.to_dict() for place in city.places])
        else:
            new_dict = request.get_json()
            if new_dict:
                if not new_dict.get("user_id"):
                    return make_response({"error": "Missing user_id"}, 400)
                if not storage.get(User, new_dict['user_id']):
                    abort(404)
                if not new_dict.get("name"):
                    return make_response({"error": "Missing name"}, 400)
                else:
                    place = Place(**new_dict)
                    city.places.append(place)
                    place.save()
                    place_dict = place.to_dict()
                    del place_dict['cities']
                    return make_response(jsonify(place_dict), 201)
            else:
                return make_response({"error": "Not a JSON"}, 400)
    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def place_byid(place_id):
    place = storage.get(Place, place_id)
    if place:
        if request.method == "GET":
            return jsonify(place.to_dict())
        elif request.method == "DELETE":
            place.delete()
            storage.save()
            return jsonify({})
        else:
            new_dict = request.get_json()
            if new_dict:
                for k, v in new_dict.items():
                    if k not in ['id', 'user_id', 'city_id',
                                 'created_at', 'updated_at']:
                        setattr(place, k, v)
                place.save()
                return jsonify(place.to_dict())
            else:
                return make_response({"error": "Not a JSON"}, 400)
    abort(404)


def getPlacesFromCities(city, all_places):
    """helper function for places search"""
    for place in city.places:
        if place not in all_places:
            all_places.append(place)


@app_views.route("/places_search", strict_slashes=False,
                 methods=["POST"])
def place_search():
    data = request.get_json()
    if not data:
        return make_response({"error": "Not a JSON"}, 400)
    states = []
    cities = []
    amenities = []
    for state_id in data.get('states', []):
        state = storage.get(State, state_id)
        if state:
            states.append(state)
    for city_id in data.get('cities', []):
        city = storage.get(City, city_id)
        if city:
            cities.append(city)
    for amenity_id in data.get('amenities', []):
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            amenities.append(amenity)

    places = storage.all(Place)
    if len(states) == len(cities) == len(amenities) == 0:
        return jsonify([place.to_dict()
                       for place in places.values()])
    all_places = []
    print(cities)
    for city in cities:
        all_places = getPlacesFromCities(city, all_places)
    for state in states:
        for city in state.cities:
            all_places = getPlacesFromCities(city, all_places)
    filterd_places = []
    for place in all_places:
        take = True
        for amenity in amenities:
            if amenity not in place.amenities:
                take = False
                break
        if take:
            filterd_places.append(place)

    return jsonify([place.to_dict()
                    for place in filterd_places])
