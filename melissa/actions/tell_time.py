from datetime import datetime

# Melissa
from melissa.tts import tts

WORDS = {
  'what_is_time': {'groups': ['time']},
  'what_is_date': {'groups': ['date']},
  'what_is_day': {'groups': ['day']}
}


def what_is_time(text):
    tts("The time is " + datetime.strftime(datetime.now(), '%H:%M:%S'))


def what_is_date(text):
    tts("The date is " + datetime.strftime(datetime.now(), '%m/%d/%Y'))


def what_is_day(text):
    tts("The day is " + datetime.strftime(datetime.now(), '%A'))
