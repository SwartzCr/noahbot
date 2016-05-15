from twython import Twython
from twython import TwythonStreamer
import json

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
        if 'grape ' in data['text']:
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
