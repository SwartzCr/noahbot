from twython import Twython
from twython import TwythonStreamer
import json
import random

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            do_twitter(data)
    def on_error(self, status_code, data):
        print status_code
        #self.disconnect()

def do_twitter(data):
    twitter = auth()
    if data['user']['screen_name'] == "pomological":
        if 'grapes' in data['text']:
            retweet(twitter, data)
    if data['user']['screen_name'].lower() == "tinydungeons":
        if not random.randrange(0,30):
            retweet(twitter, data)
    if data['user']['screen_name'].lower() == "hard_to_yelp":
        if not random.randrange(0,30):
            retweet(twitter, data)
    if data['user']['screen_name'] == 'hintline':
        if not random.randrange(0, 30):
            retweet(twitter, data)
    if data['user']['screen_name'] == 'xor':
        if not random.randrange(0, 100):
            twitter.update_status(status="@xor parker", in_reply_to_status_id=data['id'])
    if data['in_reply_to_screen_name'] == "swartzcr":
        if not random.randrange(0,5):
            twitter.update_status(status="@{0} oh hi!".format(data['user']['screen_name']))

        elif not random.randrange(0,10):
            twitter.update_status(status="@{0} hmmmmm".format(data['user']['screen_name']))
    if not random.randrange(0,1000):
        retweet(twitter, data)
    if not random.randrange(0,1000):
        twitter.create_favorite(id=data['id'])

def retweet(twitter, data):
    twitter.retweet(id=data['id'])

def auth():
    with open("access.json", 'r') as f:
        db = json.load(f)
    return Twython(db["API_Key"], db["API_Secret"], db["Access_Token"], db["Access_Token_Secret"])


def auth_streamer():
    with open("access.json", 'r') as f:
        db = json.load(f)
    return TweetStreamer(db["API_Key"], db["API_Secret"], db["Access_Token"], db["Access_Token_Secret"])

def main():
    twitter = auth_streamer()
    twitter.user()

if __name__ == "__main__":
    main()
