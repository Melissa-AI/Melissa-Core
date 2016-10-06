# Melissa
from melissa.tts import tts


WORDS = {'spell_text': {'groups': ['spell']}}


def spell_text(text):
    text = list(text.split(' ', 1)[1])
    spelling = ' '.join(text)
    tts(spelling)
