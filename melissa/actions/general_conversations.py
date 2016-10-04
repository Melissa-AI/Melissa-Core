import random

# Melissa
from melissa import profile
from melissa.tts import tts

WORDS={'who_are_you': {'groups': [['who', 'are', 'you']]},
       'toss_coin': {'groups': [['heads', 'tails'], ['toss', 'coin'], ['flip', 'coin']]},
       'how_am_i': {'groups': [['how', 'i', 'look'],['how', 'am', 'i']]},
       'tell_joke': {'groups': [['tell', 'joke']]},
       'who_am_i': {'groups': [['who', 'am', 'i']]},
       'where_born': {'groups': [['where', 'born']]},
       'how_are_you': {'groups': [['how', 'are', 'you']]},
       'are_you_up': {'groups': [['you', 'up']]},
       'undefined': {'groups': []},
      }

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
    replies =['You are goddamn handsome!', 'My knees go weak when I see you.', 'You are sexy!', 'You look like the kindest person that I have met.']
    tts(random.choice(replies))

def tell_joke(text):
    jokes = ['What happens to a frogs car when it breaks down? It gets toad away.', 'Why was six scared of seven? Because seven ate nine.', 'Why are mountains so funny? Because they are hill areas.', 'Have you ever tried to eat a clock? I hear it is very time consuming.', 'What happened when the wheel was invented? A revolution.', 'What do you call a fake noodle? An impasta!', 'Did you hear about that new broom? It is sweeping the nation!', 'What is heavy forward but not backward? Ton.',  'No, I always forget the punch line.']
    tts(random.choice(jokes))

def who_am_i(text):
    tts('You are ' + profile.data['name'] + ', a brilliant person. I love you!')

def where_born(text):
    tts('I was created by a magician named Tanay, in India, the magical land of himalayas.')

def how_are_you(text):
    tts('I am fine, thank you.')

def are_you_up(text):
    tts('For you sir, always.')

def undefined(text):
    tts('I dont know what that means!')
