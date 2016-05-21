# coding=utf-8
from flask import Blueprint, render_template, current_app

view = Blueprint('view', __name__)


@view.route('/', methods=['GET'])
@view.route('/<path:path>', methods=['GET'])
def index(path='index'):
    current_app.logger.info(u'访问 => /' + path)
    return render_template('index.html')