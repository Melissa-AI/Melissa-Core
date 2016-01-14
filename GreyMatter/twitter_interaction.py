import tweepy

from SenseCells.tts import tts

def post_tweet(speech_text, consumer_key, consumer_secret, access_token, access_token_secret):

    words_of_message = speech_text.split()
    words_of_message.remove('tweet')
    cleaned_message = ' '.join(words_of_message).capitalize()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    api.update_status(status=cleaned_message)

    tts('Your tweet has been posted')

