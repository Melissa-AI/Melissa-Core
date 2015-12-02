import tweepy

from SenseCells.tts import tts

def my_tweets():
    # This needs formatting, not currently fit to be run.
    tts('Loading your tweets, ' + name)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    timeline = api.user_timeline(count=10, include_rts=True)