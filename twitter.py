import os
import webbrowser
from twython import Twython, TwythonStreamer
from collections import Counter
CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
temp_client = Twython(CONSUMER_KEY, CONSUMER_SECRET)
temps_creds = temp_client.get_authentication_tokens()
url = temps_creds['auth_url']

print(f"go visit {url} and get the pin and paste it below")
webbrowser.open(url)
PIN_CODE = input("pin")
auth_client = Twython(CONSUMER_KEY, CONSUMER_SECRET, temps_creds['oauth_token'],
temps_creds['oauth_token_secret'])
final_step= auth_client.get_authorized_tokens(PIN_CODE)
ACCESS_TOKEN = final_step['oauth_token']
ACCESS_TOKEN_SECRET = final_step['oauth_token_secret']

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

for status in twitter.search(q='"data science"')["statuses"]:
    user = status["user"]["screen_name"]
    text = status["text"]
    print(f"{user}:{text}\n")

tweets = []

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if data.get('lang') == 'en':
            tweets.append(data)
            print(f"received tweet #{len(tweets)}")
        if len(tweets)>=100:
            self.disconnect()
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
stream.statuses.filter(track='data')

top_hashtags = Counter(hashtag['text'].lower() for tweet in tweets for hashtag in tweet["entities"]["hashtags"])
print(top_hashtags)
