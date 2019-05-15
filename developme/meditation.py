from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db


meditation = Blueprint('meditation', __name__)

@meditation.route('/meditation')
def timer():
    return render_template('meditation.html')
