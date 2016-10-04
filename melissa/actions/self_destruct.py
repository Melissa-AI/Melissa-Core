import subprocess

# Melissa
from melissa.tts import tts

WORDS = {'self_destruct': {'groups': [['self', 'destruct']]}}


def self_destruct(text):
    tts('Self destruction mode engaged, over and out.')
    subprocess.call(['sudo', 'rm', '-r', '../Melissa-Core'])
    quit()
