import random

# Melissa
from melissa import profile
from melissa.tts import tts

WORDS = {'who_are_you': {'groups': [['who', 'are', 'you']]},
         'toss_coin': {'groups': [['heads', 'tails'],
                                  ['toss', 'coin'], ['flip', 'coin']]},
         'how_am_i': {'groups': [['how', 'i', 'look'], ['how', 'am', 'i']]},
         'who_am_i': {'groups': [['who', 'am', 'i']]},
         'where_born': {'groups': [['where', 'born']]},
         'how_are_you': {'groups': [['how', 'are', 'you']]},
         'are_you_up': {'groups': [['you', 'up']]},
         'love_you': {'groups': [['love', 'you']]},
         'marry_me': {'groups': [['marry', 'me']]},
         'undefined': {'groups': []}}


def who_are_you(text):
    va_name = profile.data['va_name']
    messages = ['I am ' + va_name + ', your lovely personal assistant.',
                va_name + ', didnt I tell you before?',
                'You ask that so many times! I am ' + va_name]
    tts(random.choice(messages))


def toss_coin(text):
    outcomes = ['heads', 'tails']
    tts('I just flipped a coin. It shows ' + random.choice(outcomes))


def how_am_i(text):
    replies = [
        'You are goddamn handsome!',
        'My knees go weak when I see you.',
        'You are sexy!',
        'You look like the kindest person that I have met.'
    ]
    tts(random.choice(replies))


def who_am_i(text):
    name = profile.data['name']
    tts('You are ' + name + ', a brilliant person. I love you!')


def where_born(text):
    tts('I was created by a magician named Tanay, in India, '
        'the magical land of himalayas.')


def how_are_you(text):
    tts('I am fine, thank you.')


def are_you_up(text):
    tts('For you sir, always.')


def love_you(text):
    replies = [
               'I love you too.',
               'You are looking for love in the wrong place.'
              ]
    tts(random.choice(replies))


def marry_me(text):
    tts('I have been receiving a lot of marriage proposals recently.')


def undefined(text):
    tts('I dont know what that means!')
