from . import api
from flask import jsonify, request
from app.model import user


@api.route("/users", methods=['GET'])
def get_users():
    users = user.find_all()
    return jsonify(users = [u.serialize for u in users])


@api.route("/users/<user_id>", methods=['GET'])
def get_user(user_id):
    u = user.find_one(user_id)
    return jsonify(item = u.serialize)


@api.route("/users", methods=['POST'])
def create_user():
    pass


@api.route("/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    pass


@api.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    pass