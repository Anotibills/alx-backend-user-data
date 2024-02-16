#!/usr/bin/env python3
"""
This is the User views module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    '''
    This returns list of all User objects JSON represented
    '''
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    '''
    This returns user ID
    '''
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    '''
    This returns the user ID and the pass code sign
    '''
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    '''
    This returns user ID or error, if any character is missing
    '''
    rj = request.get_json()
    if not rj or not rj.get("email"):
        return jsonify({'error': "email missing"}), 400
    if not rj.get("password"):
        return jsonify({'error': "password missing"}), 400

    user = User(email=rj.get("email"),
                password=rj.get("password"),
                first_name=rj.get("first_name"),
                last_name=rj.get("last_name"))
    try:
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    '''
    This returns exceptions
    '''
    user = User.get(user_id)
    if user is None:
        abort(404)

    rj = request.get_json()
    if not rj:
        return jsonify({'error': "Wrong format"}), 400

    if 'first_name' in rj:
        user.first_name = rj['first_name']
    if 'last_name' in rj:
        user.last_name = rj['last_name']

    try:
        user.save()
        return jsonify(user.to_json()), 200
    except Exception as e:
        return jsonify({'error': f"Can't update User: {e}"}), 400
