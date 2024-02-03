#!/usr/bin/python3
""" objects that handles all Amenities Objects"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def all_amenities():
    """Retrieves a list of all amenities objects"""
    response = []
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        response.append(amenity.to_dict())
    return jsonify(response)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an amenity object"""
    response = storage.get(Amenity, amenity_id)
    if response is None:
        abort(404)
    return jsonify(response.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Deletes an amenity  Object"""
 if amenity_id is None:
        abort(404)
    else:
        trash = storage.get(Amenity, amenity_id)
        if trash is not None:
            storage.delete(trash)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an amenity object"""
    try:
        new = request.get_json()
    except Exception:
        pass
    if new is None or type(new) is not dict:
        abort(400, 'Not a JSON')
    if 'name' not in new.keys():
        abort(400, 'Missing Name')
    response = Amenity(**new)
    response.save()
    return make_response(jsonify(response.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """Updates an amenity objects"""
     response = storage.get(Amenity, amenity_id)
    if amenity_id is None or response is None:
        abort(404)
    try:
        new = request.get_json()
    except Exception:
        pass
    if new is None or type(new) is not dict:
        abort(400, 'Not a JSON')
    for key in new.keys():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(response, key, new[key])
    response.save()
    return make_response(jsonify(response.to_dict()), 200)
