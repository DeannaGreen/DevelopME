import twitter
import json
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from . import config

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


newsfeed = Blueprint('newsfeed', __name__)

@newsfeed.route('/newsfeed')
def tweets():

    OAUTH_TOKEN = config.CODE_CONFIG['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = config.CODE_CONFIG['OAUTH_TOKEN_SECRET']
    CONSUMER_KEY = config.CODE_CONFIG['CONSUMER_KEY']
    CONSUMER_SECRET = config.CODE_CONFIG['CONSUMER_SECRET']

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)

    # print(twitter_api)

    q = '#coding'

    count = 20

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets

    search_results = twitter_api.search.tweets(q=q, count=count)

    statuses = search_results['statuses']

    # print(statuses)

    # Iterate through 5 more batches of results by following the cursor

    for _ in range(20):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError: # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

    print(statuses)

    status_texts = [ status['text']
                     for status in statuses ]

    screen_names = [ user_mention['screen_name']
                     for status in statuses
                         for user_mention in status['entities']['user_mentions'] ]

    hashtags = [ hashtag['text']
                 for status in statuses
                     for hashtag in status['entities']['hashtags'] ]

    # Compute a collection of all words from all tweets
    words = [ w
              for t in status_texts
                  for w in t.split() ]


    # Explore the first 5 items for each...

    print(json.dumps(status_texts[0:20], indent=1))
    # print(json.dumps(screen_names[0:5], indent=1))
    # print(json.dumps(hashtags[0:5], indent=1))
    # print(json.dumps(words[0:5], indent=1))
    return render_template('twitter.html', status_texts=status_texts, screen_names=screen_names, statuses=statuses)


# @newsfeed.route('/newsfeed2')
# def tweets2():
#     ckey="fL3xczernPD5heWfqvieb8cPK"
#     csecret="Y8ctl29Lm5byRVPABOJE22gsfbSxbIAf6XANWfMKkkg1Zl0Yzw"
#     atoken="997779978-r542hm7EbxICcvZiSydwbqLfUj5SAwzTm70UjKqx"
#     asecret="v2ESQnOdLOndvh2bizZvVl9iaDp7oOz6kSYrgdjF7IIAx"
#
#     auth = OAuthHandler(ckey, csecret)
#     auth.set_access_token(atoken, asecret)
#
#     twitterStream = Stream(auth, listener())
#     twitterStream.filter(track=["coding"])
#
#     return "done"
#
#
# class listener(StreamListener):
#
#     def on_data(self, data):
#         print(data)
#         return(True)
#
#     def on_error(self, status):
#         print(status)