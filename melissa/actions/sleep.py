import random

# Melissa
from melissa import profile
from melissa.tts import tts

WORDS = {'go_to_sleep': {'groups': ['sleep', 'bye', 'deactivate', 'stop',
         'suspend', 'quit', ['power', 'off'], ['stand', 'down'],
         ['good', 'bye']]}}


def go_to_sleep(text):
    replies = ['See you later!', 'Just call my name and I\'ll be there!']
    tts(random.choice(replies))

    if profile.data['hotword_detection'] == 'on':
        print('\nListening for Keyword...')
        print('Press Ctrl+C to exit')

    quit()
