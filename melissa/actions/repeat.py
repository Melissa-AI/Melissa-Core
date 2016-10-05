# Melissa
from melissa.tts import tts


WORDS = {'repeat_text': {'groups': ['repeat', 'say']}}


def repeat_text(text):
    text = text.split(' ', 1)[1]
    tts(text)
