import tweepy

# Melissa
from melissa import profile
from melissa.tts import tts

WORDS = {'post_tweet': {'groups': ['tweet']}}


def post_tweet(text):

    if profile.data['twitter']['consumer_key'] == "xxxx" \
            or profile.data['twitter']['consumer_secret'] == "xxxx" \
            or profile.data['twitter']['access_token'] == "xxxx" \
            or profile.data['twitter']['access_token_secret'] == "xxxx":

        msg = "Twitter requires a consumer key and secret," \
              " and an access token and token secret."
        print msg
        tts(msg)
        return

    words_of_message = text.split()
    words_of_message.remove('tweet')
    cleaned_message = ' '.join(words_of_message).capitalize()

    auth = tweepy.OAuthHandler(
        profile.data['twitter']['consumer_key'],
        profile.data['twitter']['consumer_secret'])

    auth.set_access_token(
        profile.data['twitter']['access_token'],
        profile.data['twitter']['access_token_secret'])

    api = tweepy.API(auth)
    api.update_status(status=cleaned_message)

    tts('Your tweet has been posted')
