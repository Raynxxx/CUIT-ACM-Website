from . import api
from flask import jsonify, request
from app.model import user
from app.util.decorators import require_auth


@api.route("/users", methods=['GET'])
@require_auth
def get_users():
    users = user.find_all()
    return jsonify(users=[u.serialize for u in users])


@api.route("/users/<user_id>", methods=['GET'])
@require_auth
def get_user(user_id):
    u = user.find_one(user_id)
    return jsonify(item=u.serialize)


@api.route("/users", methods=['POST'])
@require_auth
def create_user():
    pass


@api.route("/users/<user_id>", methods=['PUT'])
@require_auth
def update_user(user_id):
    pass


@api.route("/users/<user_id>", methods=['DELETE'])
@require_auth
def delete_user(user_id):
    pass