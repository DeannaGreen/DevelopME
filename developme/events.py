from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from developme import db
# from developme import config
import meetup.api
import requests
import json
import os

events = Blueprint('events', __name__)

@events.route('/meetup')
@login_required

def list():
    meetup_key = os.environ.get('MEETUP_KEY', None)
    try:
        location = request.args.get('location')
    except NameError:
        location = None

    if location is None:
        event_list = []
        city_name = ""
    else:
        client = meetup.api.Client(meetup_key)
        city_data = requests.get("https://api.meetup.com/find/locations?&sign=true&photo-host=public&query="+location+"&key="+meetup_key)
        if len(city_data.json()) is 0:
            flash('Cant find that city')
            event_list = []
            city_name = ""
        else:
            city = city_data.json()[0]
            city_name = city["name_string"]
            df = requests.get("https://api.meetup.com/find/upcoming_events?&sign=true&photo-host=public&lon="+str(city["lon"])+"&topic_category=34&page=20&radius=50&lat="+str(city["lat"])+"&order=best&key="+meetup_key)
            data = df.json()
            event_list = data["events"]

    # for event in data["events"]:
    #     print("-----------")
    #     print(event["name"])
    #     print(event["local_date"])
    #     print(event["local_time"])

    return render_template('events.html', event_list=event_list, city=city_name)

@events.route('/meetup', methods=['POST'])
@login_required
def list_post():
    city = request.form.get('city')
    return redirect(url_for('events.list', location=city))
