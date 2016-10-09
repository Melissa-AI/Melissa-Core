# Melissa
from melissa import profile
from melissa.tts import tts
from melissa.stt import stt
from melissa.brain import query


def main():
    tts('Welcome ' + profile.data['name'] +
        ', systems are now ready to run. How can I help you?')

    while True:
        text = stt()

        if text is None:
            continue
        else:
            query(text)

main()
