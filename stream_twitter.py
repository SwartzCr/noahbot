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
        if not random.randrange(0,100):
            retweet(twitter, data)
    #if data['user']['screen_name'].lower() == "nice_domains":
    #    if not random.randrange(0,40):
    #        retweet(twitter, data)
    if data['user']['screen_name'].lower() == "hard_to_yelp":
        if not random.randrange(0,70):
            retweet(twitter, data)
    #if data['user']['screen_name'] == 'hintline':
    #    if not random.randrange(0, 100):
    #        retweet(twitter, data)
    if data['user']['screen_name'] == 'xor':
        if 'retweeted_status' in data.keys():
            if not data['retweeted_status']['user']['screen_name'] =='xor':
                return
        if not random.randrange(0, 100):
            twitter.update_status(status="@xor parker", in_reply_to_status_id=data['id'])
    if "quinoa" in data['text'].lower():
        retweet(twitter, data)
    if data['in_reply_to_screen_name'].lower() == "swartzcr":
        if ["yo"] == [txt.lower() for txt in data['text'].split() if not txt.startswith("@")]:
            reply_to = [txt for txt in data['text'].split() if txt.startswith("@")]
            reply_to.remove("@SwartzCr")
            instigator = data["user"]["screen_name"]
            reply_to.append("@{0}".format(instigator))
            message = " ".join(reply_to)
            message += " yo"
            twitter.update_status(status=message, in_reply_to_status_id=data['id'])
       # elif not random.randrange(0,5):
       #     twitter.update_status(status="@{0} oh hi!".format(data['user']['screen_name']))
       # elif not random.randrange(0,10):
       #     twitter.update_status(status="@{0} hmmmmm".format(data['user']['screen_name']))
    if not random.randrange(0,2000):
        retweet(twitter, data)
    if not random.randrange(0,2000):
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
