# coding=utf-8
from . import api
from app.util.token import generate_token
from flask import request, jsonify
from app.model import user


@api.route('/login', methods=['POST'])
def login():
    incoming = request.get_json()
    u = user.find_one_by_username(incoming['username'])
    if not u:
        return jsonify(error=True, text=u'用户不存在'), 403
    elif not u.verify_password(incoming['password']):
        return jsonify(error=True, text=u'密码输入错误'), 403
    else:
        return jsonify(token=generate_token(u))



