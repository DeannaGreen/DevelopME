from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from developme import db
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
            cities = city_data.json()
            choosen_city = None
            for city in cities:
                print(city)
                if city["country"] == 'gb':
                    choosen_city = city
                    break
            if choosen_city is None:
                choosen_city = cities[0]
            print(choosen_city)
            city_name = choosen_city["name_string"]
            df = requests.get("https://api.meetup.com/find/upcoming_events?allMeetups=false&sign=true&photo-host=public&lon="+str(choosen_city["lon"])+"&topic_category=292&page=20&radius=50&lat="+str(choosen_city["lat"])+"&order=best&fields=plain_text_description,featured_photo,group_key_photo&key="+meetup_key)
            data = df.json()
            event_list = data["events"]

        for event in data["events"]:
            if "featured_photo" in event:
                event["photo"] = event["featured_photo"]["photo_link"]
            else:
                if "key_photo" in event["group"]:
                    event["photo"] = event["group"]["key_photo"]["photo_link"]
            if "plain_text_description" not in event:
                event["plain_text_description"] = "No description provided."



    return render_template('events.html', event_list=event_list, city=city_name)

@events.route('/meetup', methods=['POST'])
@login_required
def list_post():
    city = request.form.get('city')
    return redirect(url_for('events.list', location=city))
