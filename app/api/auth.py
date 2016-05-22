# coding=utf-8
from . import api
from app.util.token import generate_token, verify_token
from app.util.decorators import verify_json
from flask import request, jsonify, current_app
from app.model import user


@api.route('/login', methods=['POST'])
@verify_json
def login():
    incoming = request.get_json()
    u = user.find_one_by_username(incoming['username'])
    if not u:
        return jsonify(error=True, text=u'用户不存在')
    elif not u.verify_password(incoming['password']):
        return jsonify(error=True, text=u'密码输入错误')
    else:
        return jsonify(token=generate_token(u))


@api.route('/check_token', methods=['POST'])
@verify_json
def check_token():
    incoming = request.get_json()
    ret = verify_token(incoming['token'])
    if ret:
        return jsonify(valid=True, data=ret)
    else:
        return jsonify(valid=False, text=u'认证失败'), 403



