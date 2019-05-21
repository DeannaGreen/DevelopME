import twitter
import json
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
import os
from datetime import datetime

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


newsfeed = Blueprint('newsfeed', __name__)

@newsfeed.route('/newsfeed')
@login_required
def tweets():

    OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN', None)
    OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET', None)
    CONSUMER_KEY = os.environ.get('CONSUMER_KEY', None)
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)

    q = '#coding'

    count = 20

    search_results = twitter_api.search.tweets(q=q, count=count)

    statuses = search_results['statuses']

    for _ in range(20):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError:
            break

        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

    # print(statuses)

    status_texts = [ status['text']
                     for status in statuses ]

    screen_names = [ user_mention['screen_name']
                     for status in statuses
                         for user_mention in status['entities']['user_mentions'] ]

    hashtags = [ hashtag['text']
                 for status in statuses
                     for hashtag in status['entities']['hashtags'] ]

    words = [ w
              for t in status_texts
                  for w in t.split() ]

    dates = [ (status['created_at'])[0:19]
                     for status in statuses ]

    # print(json.dumps(status_texts[0:20], indent=1))

    return render_template('twitter.html', status_texts=status_texts, screen_names=screen_names, statuses=statuses,)
