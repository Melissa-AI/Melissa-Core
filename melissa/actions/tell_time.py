from datetime import datetime

# Melissa
from melissa.tts import tts

WORDS = {'what_is_time': {'groups': ['time']}}


def what_is_time(text):
    tts("The time is " + datetime.strftime(datetime.now(), '%H:%M:%S'))
