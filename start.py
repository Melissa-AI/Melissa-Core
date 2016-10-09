import sys
import subprocess

# Melissa
from melissa import profile
from melissa.tts import tts
from melissa.stt import stt
from melissa.brain import query


def main():
    tts('Welcome ' + profile.data['name'] +
        ', how can I help you?')

    while True:
        if sys.platform == 'darwin':
            subprocess.call(['afplay', 'data/snowboy_resources/ding.wav'])
        elif sys.platform.startswith('linux') or sys.platform == 'win32':
            subprocess.call(['mpg123', 'data/snowboy_resources/ding.wav'])

        text = stt()

        if text is None:
            continue
        else:
            query(text)

main()
