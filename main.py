from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from . import config
import random

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/gif')
@login_required
def giphy():
    return render_template('gif.html', GIPHY_KEY=config.CODE_CONFIG['GIPHY_KEY'])

@main.route('/questions')
@login_required
def questions():
    questions = [
    'Question1', 
    'Question2',
    'Question3'
    ]
    q = random.choice(questions)

    return render_template('questions.html', q=q)
