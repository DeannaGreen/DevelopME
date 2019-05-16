from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
from developme import db
from developme import config
import random

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', name=current_user.name, image_file=image_file)

@main.route('/update', methods=['POST'])
def profile_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    return redirect(url_for('main.profile'))

@main.route('/gif')
@login_required
def giphy():
    return render_template('gif.html', GIPHY_KEY=config.CODE_CONFIG['GIPHY_KEY'])

@main.route('/questions')
@login_required
def questions():
    tech_questions = [
    'Did you have a productive day yesterday?',
    'Can I help you in any way?',
    'Would you like to pair program?',
    'Did you achieve everything you wanted to yesterday?',
    'What do you want to achieve today?',
    'Any wins to celebrate this week?',
    'What challenges are you facing? Where are you stuck?',
    'What is the best thing that happened to you this week, either at work or outside of it?',
    'What were some great contributions made by other team members?',
    'Could you give me some constructive feedback?',
    'Do you prefer written or verbal communication?',
    'Which one do you prefer and why: teamwork or working alone?',
    'What is something you could teach me about?',
    'What are some of your long term goals?',
    'What goals do you have for the next five years?',
    ]
    questions = [
    'What is on your mind?',
    'What challenge are you working on today?',
    'Can I help you in any way?',
    'How are you feeling?',
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
    'Apart from the necessities, what is one thing you could not live without?',
    'If you had to describe yourself in five words, what would they be?',
    'What goals do you have for the next five years?',
    'What is the first thing you would do if you won the lottery?',
    'Where did you last go on holiday?'
    ]
    mergedlist = questions + tech_questions

    return render_template('questions.html', q=random.choice(questions), tech_q=random.choice(tech_questions), random=random.choice(mergedlist))
