# coding=utf-8
from functools import wraps
from flask import g, request, jsonify, current_app
from .token import verify_token


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token:
            string_token = token.encode('ascii', 'ignore')
            user = verify_token(string_token)
            if user:
                g.current_user = user
                return f(*args, **kwargs)
        return jsonify(message="Authentication is required"), 401
    return decorated


def verify_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        incoming = request.get_json()
        if not incoming:
            current_app.logger.error(u'错误请求 => ' + f.__name__)
            return jsonify(error=True, text=u'非法请求'), 400
        else:
            return f(*args, **kwargs)
    return decorated