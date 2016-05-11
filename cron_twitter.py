from twython import Twython
import json
import random

def auth():
    with open("access.json", 'r') as f:
        db = json.load(f)
    return Twython(db["API_Key"], db["API_Secret"], db["Access_Token"], db["Access_Token_Secret"])

def load_text():
    with open("descriptions.json", 'r') as f:
        out = json.load(f)
    return random.choice(out)

def load_friends():
    with open("friends.json", 'r') as f:
        out = json.load(f)
    return out

def update_description(twitter):
    text = load_text()
    twitter.update_profile(description=text)

def update_friends(cur_friends):
    with open("friends.json", 'w') as f:
        json.dump(cur_friends, f)

def fix_unfollow(userid, twitter):
    text = ""
    try:
        user = twitter.create_friendship(user_id=userid)
        text = "WTF @twitter, unfollow bug just made me unfollow @{0} :(".format(user['screen_name'])
    except:
        text = "huh, I unfollowed user {0}".format(userid)
    if text:
        twitter.update_status(status = text)

def check_friends(twitter):
    prev_friends = set(load_friends())
    cur_friends = twitter.get_friends_ids(count=400)['ids']
    update_friends(cur_friends)
    cur_friends = set(cur_friends)
    for user in prev_friends.difference(cur_friends):
        fix_unfollow(user, twitter)



def main():
    twitter = auth()
    update_description(twitter)
    check_friends(twitter)

if __name__ == "__main__":
    main()
