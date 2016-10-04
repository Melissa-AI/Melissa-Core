import subprocess

# Melissa
from melissa.tts import tts

WORDS = {'very_dark': {'groups': ['dark']},
         'feeling_angry': {'groups': [['feeling', 'angry']]},
         'feeling_creative': {'groups': [['feeling', 'creative']]},
         'feeling_lazy': {'groups': [['feeling', 'lazy']]},
         'turn_off': {'groups': [['lights', 'off']]}}


def very_dark(text):
    subprocess.call(['blink1-tool', '--white'])
    tts('Better now?')


def feeling_angry(text):
    subprocess.call(['blink1-tool', '--cyan'])
    tts('Calm down dear!')


def feeling_creative(text):
    subprocess.call(['blink1-tool', '--magenta'])
    tts('So good to hear that!')


def feeling_lazy(text):
    subprocess.call(['blink1-tool', '--yellow'])
    tts('Rise and shine dear!')


def turn_off(text):
    subprocess.call(['blink1-tool', '--off'])
