import signal
import subprocess

# Melissa
from melissa import profile
from melissa.utilities import snowboydecoder

interrupted = False
subprocess.call(['python', 'start.py'])


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def melissa_activate():
    subprocess.call(['python', 'start.py'])

model = 'data/snowboy_resources/Melissa.pmdl'

signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

if profile.data['hotword_detection'] == 'on':
    detector.start(detected_callback=melissa_activate,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    detector.terminate()
