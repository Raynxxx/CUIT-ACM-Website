from . import view
from flask import render_template


@view.route('/admin', methods=['GET'])
def index():
    return render_template('admin.html')