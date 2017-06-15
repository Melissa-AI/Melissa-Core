import sys
import subprocess

# Melissa
from melissa.profile_loader import load_profile
from melissa.tts import tts
from melissa.stt import stt
from melissa.brain import query


def main():
    data = load_profile(True)
    tts('Welcome ' + data['name'] +
        ', how can I help you?')

    while True:
        if sys.platform == 'darwin':
            subprocess.call(['afplay', 'data/snowboy_resources/ding.wav'])
        elif sys.platform.startswith('linux') or sys.platform == 'win32':
            try:
                subprocess.call(['mpg123', 'data/snowboy_resources/ding.wav'])
            except OSError:
                subprocess.call(
                    ['mpg123', 'data/snowboy_resources/ding.wav'], shell=True)

        text = stt()

        if text is None:
            continue
        else:
            query(text)

if __name__ == "__main__":
    main()
