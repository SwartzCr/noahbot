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

def fix_unfollow(user, friends_list, twitter):
    user_data = [friend for friend in friends_list if friend['id']==user][0]
    screen_name = user_data["screen_name"]
    blocked = user_data["blocked_by"]
    text = ""
    tag = "unfollow"
    if blocked:
        text = "oh cool, @{0} blocked me :/ #{1}".format(screen_name, tag)
    else:
       try:
           _ = twitter.create_friendship(user_id=user)
           text = "WTF @twitter, unfollow bug just made me unfollow @{0} :( #{1}".format(screen_name, tag)
       except:
           text = "huh, I unfollowed @{0} - maybe they deleted their account? #{1}".format(screen_name, tag)
    if text:
        twitter.update_status(status = text)

def make_friends_list(twitter):
    next_cursor = -1
    cur_friends_list = []
    while next_cursor:
        temp = twitter.get_friends_list(count="200", cursor=next_cursor)
        cur_friends_list.extend(temp['users'])
        next_cursor = temp['next_cursor']
    return cur_friends_list

def serialize_ids(friends_list):
    return set([user['id'] for user in friends_list])


def check_friends(twitter):
    prev_friends_list = load_friends()
    prev_friends = serialize_ids(prev_friends_list)
    cur_friends_list = make_friends_list(twitter)
    update_friends(cur_friends_list)
    cur_friends = serialize_ids(cur_friends_list)
    for user in prev_friends.difference(cur_friends):
        fix_unfollow(user, prev_friends_list, twitter)



def main():
    twitter = auth()
    update_description(twitter)
    check_friends(twitter)

if __name__ == "__main__":
    main()
