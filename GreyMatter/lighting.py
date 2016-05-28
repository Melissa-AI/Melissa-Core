import subprocess

from SenseCells.tts import tts

def very_dark():
    subprocess.call(['blink1-tool', '--white'])
    tts('Better now?')

def feeling_angry():
    subprocess.call(['blink1-tool', '--cyan'])
    tts('Calm down dear!')

def feeling_creative():
    subprocess.call(['blink1-tool', '--magenta'])
    tts('So good to hear that!')

def feeling_lazy():
    subprocess.call(['blink1-tool', '--yellow'])
    tts('Rise and shine dear!')

def turn_off():
    subprocess.call(['blink1-tool', '--off'])
