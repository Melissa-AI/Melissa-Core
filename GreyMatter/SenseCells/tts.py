import sys
import subprocess

def tts(message):
    """
    This function takes a message as an argument and converts it to speech depending on the OS.
    """
    if sys.platform == 'darwin':
        tts_engine = 'say'
        return subprocess.call([tts_engine, message])
    elif sys.platform == 'linux2' or sys.platform == 'linux' or sys.platform == 'win32':
        tts_engine = 'espeak'
        language = '-ven+f4'
        speed = '-s170'
        return subprocess.call([tts_engine, language, speed, message])
