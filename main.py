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
    'Did you have a productive day yesterday?',
    'What is on your mind?',
    'What challenge are you working on today?',
    'Can I help you in any way?',
    'Would you like to pair program?',
    'Did you achieve everything you wanted to yesterday?',
    'What do you want to achieve today?',
    'Any wins to celebrate this week?',
    'What challenges are you facing? Where are you stuck?',
    'How are you feeling?',
    'What is the best thing that happened to you this week, either at work or outside of it?',
    'What were some great contributions made by other team members?',
    'Could you give me some constructive feedback?',
    'Do you prefer written or verbal communication?',
    'Which one do you prefer and why: teamwork or working alone?',
    'If your life was a book, what would it be called?',
    'Do you like to cook?',
    'Where do you like to go when you eat out?',
    'What is on your bucket list?',
    'What is something you could teach me about?',
    'If you were stranded on a desert island what would be the one item you bring?',
    'Do you prefer cats or dogs?',
    'What are some of your long term goals?',
    'What is the most useful thing you own?',
    'What is your spirit animal?',
    'If you could have lunch with one person dead or alive, who would it be?',
    'If you could only eat one food for the rest of your life what would it be?',
    'What makes you laugh the most?',
    'Apart fro the necessities, what is one thing you could not live without?',
    'If you had to describe yourself in five words, what would they be?',
    'What goals do you have for the next five years?',
    'What is the first thing you would do if you won the lottery?',
    'Where did you last go on holiday?'
    ]
    q = random.choice(questions)

    return render_template('questions.html', q=q)
