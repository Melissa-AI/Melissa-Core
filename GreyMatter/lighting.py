import os

from SenseCells.tts import tts

def very_dark():
    os.system('blink1-tool --white')
    tts('Better now?')

def feeling_angry():
    os.system('blink1-tool --cyan')
    tts('Calm down dear!')

def feeling_creative():
    os.system('blink1-tool --magenta')
    tts('So good to hear that!')

def feeling_lazy():
    os.system('blink1-tool --yellow')
    tts('Rise and shine dear!')

def turn_off():
    os.system('blink1-tool --off')
