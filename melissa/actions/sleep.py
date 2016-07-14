# Melissa
from melissa.tts import tts

WORDS = {'go_to_sleep': {'groups': ['sleep','bye','exit','stop','close',
                                    'quit',['good','bye']]}}

def go_to_sleep(text):
    tts('Goodbye! Have a great day!')
    quit()
