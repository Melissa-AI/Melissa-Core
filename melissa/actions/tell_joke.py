# To register more APIs create a function which calls the joke API and
# append the function name to the jokeAPIRegister list. Which is used to
# randomly select one of the APIs

import random
import requests
import json

# Melissa
from melissa.tts import tts

WORDS = {'tell_joke': {'groups': [['tell', 'joke']]}}


def chuck_norris():
    while (True):
        req = requests.get('http://api.icndb.com/jokes/random')
        json_joke = json.loads(req.text)['value']
        if json_joke[u'categories'] != u'explicit':
            return json_joke[u'joke']


def in_house():
    jokes = [
        'What happens to a frogs car when it breaks down? It gets toad away.',
        'Why was six scared of seven? Because seven ate nine.',
        'Why are mountains so funny? Because they are hill areas.',
        'Have you ever tried to eat a clock?'
        'I hear it is very time consuming.',
        'What happened when the wheel was invented? A revolution.',
        'What do you call a fake noodle? An impasta!',
        'Did you hear about that new broom? It is sweeping the nation!',
        'What is heavy forward but not backward? Ton.',
        'No, I always forget the punch line.'
    ]
    return random.choice(jokes)


jokeAPIRegister = [chuck_norris, in_house]


def tell_joke(text):
    tts(random.choice(jokeAPIRegister)())
