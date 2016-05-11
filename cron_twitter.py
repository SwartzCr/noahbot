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

def update_description(twitter):
    text = load_text()
    twitter.update_profile(description=text)


def main():
    twitter = auth()
    update_description(twitter)

if __name__ == "__main__":
    main()
